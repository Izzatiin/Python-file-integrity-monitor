# 🛡️ Advanced File Integrity Monitor (FIM)

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue?style=for-the-badge&logo=python)
![Security Focus](https://img.shields.io/badge/Security-Blue%20Team-red?style=for-the-badge&logo=shield)
![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)

**Advanced File Integrity Monitor (FIM)** adalah alat pemantau integritas berkas berbasis Python yang dirancang untuk kebutuhan Security Engineering dan Incident Response. Tool ini berfungsi untuk mendeteksi perubahan, penambahan, atau penghapusan berkas secara akurat menggunakan algoritma cryptographic hashing modern.

---

## ✨ Fitur Utama

- 🚀 **Multi-Threaded Hashing:** Pemindaian direktori secara paralel yang cepat untuk jumlah file besar.
- 🔐 **Multi-Algorithm Support:** Mendukung algoritma cryptographic hashing SHA-256, SHA-512, dan BLAKE2b.
- 📊 **Rich Terminal UI:** Tampilan konsol interaktif lengkap dengan progress bar dan laporan status berupa tabel berwarna.
- 💾 **JSON Baseline Database:** Menyimpan data acuan (snapshot) integritas awal sistem secara terstruktur.
- 🚨 **Real-time Alerting:** Mengidentifikasi secara tepat status file yang MODIFIED (Diubah), CREATED (Baru), atau DELETED (Dihapus).

---

## 🛠️ Prasyarat & Instalasi

Pastikan Anda telah menginstal **Python 3.10+**.

1. **Clone Repositori ini:**
   `git clone https://github.com/Izzatiin/Python-file-integrity-monitor.git`
   `cd Python-file-integrity-monitor`

2. **Instal Dependencies:**
   `pip install rich`

---

## 📖 Panduan Cara Penggunaan

### 1. Inisialisasi Baseline Database (`--init`)
Sebelum melakukan pemantauan, Anda harus membuat berkas acuan (*baseline*) awal dari direktori yang ingin dipantau.

`python fim_advanced.py -t <NAMA_FOLDER_TARGET> --init`

*Contoh:*
`python fim_advanced.py -t ./my_folder --init`

---

### 2. Jalankan Pemeriksaan Integritas (`--check`)
Bandingkan kondisi direktori saat ini dengan *baseline* yang telah disimpan sebelumnya:

`python fim_advanced.py -t <NAMA_FOLDER_TARGET> --check`

*Contoh:*
`python fim_advanced.py -t ./my_folder --check`

---

### 3. Opsi Tambahan

- **Mengubah Algoritma Hashing (`-a`):**
  `python fim_advanced.py -t ./my_folder -a blake2b --init`

- **Menentukan Nama File Baseline Custom (`-b`):**
  `python fim_advanced.py -t ./my_folder -b my_baseline.json --init`

---

## 🖥️ Contoh Tampilan Laporan Audit

| Status Audit | Relative File Path |
| :---: | :--- |
| **MODIFIED** | `config/settings.json` |
| **CREATED** | `logs/unauthorized_script.py` |
| **DELETED** | `system/backup.db` |

> **Ringkasan Alert:** Modifikasi: 1 | Ditambahkan: 1 | Dihapus: 1

---

## 📝 Lisensi

Distribusikan di bawah lisensi MIT. Lihat LICENSE untuk informasi lebih lanjut.

---
*Dikembangkan oleh [Mohammad Nawfal Arfa](https://github.com/Izzatiin) — Cybersecurity & Python Enthusiast.*
