#!/usr/bin/env python3
"""
Advanced File Integrity Monitor (FIM)
Designed for Security Engineers & Incident Responders.
Year: 2026 Edition
"""

import argparse
import concurrent.futures
import hashlib
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.table import Table

console = Console()

class AdvancedFIM:
    def __init__(self, target_dir: str, baseline_file: str = "baseline.json", algorithm: str = "sha256"):
        self.target_dir = Path(target_dir).resolve()
        self.baseline_file = Path(baseline_file).resolve()
        self.algorithm = algorithm.lower()
        self.supported_algos = {"sha256": hashlib.sha256, "sha512": hashlib.sha512, "blake2b": hashlib.blake2b}
        
        if self.algorithm not in self.supported_algos:
            raise ValueError(f"Algoritma tidak didukung. Pilih: {list(self.supported_algos.keys())}")

    def _compute_hash(self, file_path: Path) -> str:
        """Menghitung hash file menggunakan chunking efisien memori."""
        hasher = self.supported_algos[self.algorithm]()
        try:
            with open(file_path, "rb") as f:
                while chunk := f.read(65536):  # 64KB Chunk
                    hasher.update(chunk)
            return hasher.hexdigest()
        except (PermissionError, FileNotFoundError):
            return "ERROR_READ_FAILED"

    def _get_all_files(self) -> list[Path]:
        """Mengumpulkan seluruh file dalam direktori target."""
        return [p for p in self.target_dir.rglob("*") if p.is_file() and p != self.baseline_file]

    def create_baseline(self):
        """Membuat baseline awal dari direktori target menggunakan multi-threading."""
        if not self.target_dir.exists():
            console.print(f"[bold red][!] Target direktori '{self.target_dir}' tidak ditemukan![/bold red]")
            return

        files = self._get_all_files()
        baseline_data = {}

        console.print(Panel(f"[bold cyan]Memulai Inisialisasi Baseline[/bold cyan]\nTarget: {self.target_dir}\nAlgoritma: {self.algorithm.upper()}", expand=False))

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=console
        ) as progress:
            task = progress.add_task("[yellow]Proses hashing file...", total=len(files))

            with concurrent.futures.ThreadPoolExecutor() as executor:
                future_to_file = {executor.submit(self._compute_hash, f): f for f in files}
                for future in concurrent.futures.as_completed(future_to_file):
                    f = future_to_file[future]
                    file_hash = future.result()
                    rel_path = str(f.relative_to(self.target_dir))
                    baseline_data[rel_path] = {
                        "hash": file_hash,
                        "size": f.stat().st_size if f.exists() else 0,
                        "last_modified": datetime.fromtimestamp(f.stat().st_mtime).isoformat() if f.exists() else ""
                    }
                    progress.advance(task)

        metadata = {
            "created_at": datetime.now().isoformat(),
            "algorithm": self.algorithm,
            "target_dir": str(self.target_dir),
            "files": baseline_data
        }

        with open(self.baseline_file, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=4)

        console.print(f"[bold green][✓] Baseline berhasil disimpan ke '{self.baseline_file.name}'! ({len(baseline_data)} file terindeks)[/bold green]\n")

    def monitor_integrity(self):
        """Membandingkan status kondisi terkini dengan baseline database."""
        if not self.baseline_file.exists():
            console.print(f"[bold red][!] File baseline '{self.baseline_file}' tidak ditemukan. Jalankan mode '--init' lebih dulu.[/bold red]")
            return

        with open(self.baseline_file, "r", encoding="utf-8") as f:
            baseline_meta = json.load(f)

        old_baseline = baseline_meta.get("files", {})
        current_files = self._get_all_files()
        current_rel_paths = {str(f.relative_to(self.target_dir)): f for f in current_files}

        modified, created, deleted = [], [], []

        # Deteksi modifikasi dan file baru
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=console
        ) as progress:
            task = progress.add_task("[cyan]Memeriksa integritas sistem...", total=len(current_files))

            with concurrent.futures.ThreadPoolExecutor() as executor:
                future_to_path = {executor.submit(self._compute_hash, f): rel_p for rel_p, f in current_rel_paths.items()}
                for future in concurrent.futures.as_completed(future_to_path):
                    rel_p = future_to_path[future]
                    curr_hash = future.result()

                    if rel_p not in old_baseline:
                        created.append(rel_p)
                    elif old_baseline[rel_p]["hash"] != curr_hash:
                        modified.append(rel_p)

                    progress.advance(task)

        # Deteksi file yang terhapus
        for old_rel_p in old_baseline.keys():
            if old_rel_p not in current_rel_paths:
                deleted.append(old_rel_p)

        # Tampilkan Hasil Scanning
        self._print_audit_report(modified, created, deleted)

    def _print_audit_report(self, modified: list, created: list, deleted: list):
        """Mencetak laporan integritas menggunakan tabel modern."""
        table = Table(title="🛡️ Laporan Pemeriksaan Integritas Sistem (FIM)", title_style="bold magenta")
        table.add_column("Status Audit", justify="center", style="bold", width=15)
        table.add_column("Relative File Path", justify="left")

        for f in modified:
            table.add_row("[yellow]MODIFIED[/yellow]", f)
        for f in created:
            table.add_row("[green]CREATED[/green]", f)
        for f in deleted:
            table.add_row("[bold red]DELETED[/bold red]", f)

        console.print("\n")
        if not modified and not created and not deleted:
            console.print(Panel("[bold green][✓] SISTEM AMAN: Tidak ditemukan perubahan integritas pada berkas![/bold green]", style="green"))
        else:
            console.print(table)
            console.print(f"\n[bold yellow]Ringkasan Alert:[/bold yellow] Modifikasi: {len(modified)} | Ditambahkan: {len(created)} | Dihapus: {len(deleted)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advanced File Integrity Monitor (FIM) - 2026 Edition")
    parser.add_argument("-t", "--target", required=True, help="Path ke direktori yang ingin dipantau")
    parser.add_argument("-b", "--baseline", default="baseline.json", help="Path file penyimpan baseline JSON")
    parser.add_argument("-a", "--algo", default="sha256", choices=["sha256", "sha512", "blake2b"], help="Algoritma hashing")
    parser.add_argument("--init", action="store_true", help="Buat baseline database baru")
    parser.add_argument("--check", action="store_true", help="Jalankan pemeriksaan integritas")

    args = parser.parse_args()

    fim = AdvancedFIM(target_dir=args.target, baseline_file=args.baseline, algorithm=args.algo)

    if args.init:
        fim.create_baseline()
    elif args.check:
        fim.monitor_integrity()
    else:
        parser.print_help()