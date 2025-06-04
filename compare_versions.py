import os
import re

# Klasörlerdeki mevcut önekleri bul
def get_available_prefixes():
    all_prefixes = set()
    folders = ["raw", "output"]
    
    for folder in folders:
        if not os.path.exists(folder):
            continue
            
        for file in os.listdir(folder):
            # mixed.txt, ips.txt veya ports.txt ile biten dosyaları bul
            match = re.match(r'^(.*?)-(mixed|ips|ports)\.txt$', file)
            if match:
                prefix = match.group(1)
                all_prefixes.add(prefix)
    
    return sorted(list(all_prefixes))

# Kullanıcıya önek seçeneklerini sun
available_prefixes = get_available_prefixes()

if not available_prefixes:
    print("Hiç önek bulunamadı. Önce script.py ile dosya oluşturun.")
    exit(1)

print("\nKullanılabilir önekler:")
for i, prefix in enumerate(available_prefixes, 1):
    print(f"{i}. {prefix}")

# Eski dosya önekini seç
while True:
    old_choice = input("\nESKİ dosya için önek seçin (numara veya isim yazın): ")
    
    # Doğrudan önek girilmiş
    if old_choice in available_prefixes:
        old_prefix = old_choice
        break
    
    # Numara girilmiş
    try:
        choice_idx = int(old_choice) - 1
        if 0 <= choice_idx < len(available_prefixes):
            old_prefix = available_prefixes[choice_idx]
            break
        else:
            print("Geçersiz numara. Lütfen listeden bir numara seçin.")
    except ValueError:
        print("Geçersiz giriş. Lütfen bir numara veya önek ismi girin.")

# Yeni dosya önekini seç
while True:
    new_choice = input("\nYENİ dosya için önek seçin (numara veya isim yazın): ")
    
    # Doğrudan önek girilmiş
    if new_choice in available_prefixes:
        new_prefix = new_choice
        break
    
    # Numara girilmiş
    try:
        choice_idx = int(new_choice) - 1
        if 0 <= choice_idx < len(available_prefixes):
            new_prefix = available_prefixes[choice_idx]
            break
        else:
            print("Geçersiz numara. Lütfen listeden bir numara seçin.")
    except ValueError:
        print("Geçersiz giriş. Lütfen bir numara veya önek ismi girin.")

# Öneklere tire ekleme
if not old_prefix.endswith('-'):
    old_prefix += '-'
if not new_prefix.endswith('-'):
    new_prefix += '-'

# Karşılaştırma çıktılarının yazılacağı klasörler
os.makedirs("raw-comparison", exist_ok=True)
os.makedirs("output-comparison", exist_ok=True)

# İşlenecek klasörler
folders = ["raw", "output"]

# Karşılaştırılabilir dosya tipleri
file_types = ["mixed.txt", "ips.txt", "ports.txt"]

print(f"\nKarşılaştırılıyor: '{old_prefix.replace('-', '')}' ile '{new_prefix.replace('-', '')}' önekli dosyalar")

# Her klasördeki dosyaları kontrol et
for folder in folders:
    files = os.listdir(folder)
    
    # Her dosya tipi için karşılaştırma yap
    for file_type in file_types:
        # Eski ve yeni dosyaları bul
        old_file = f"{old_prefix}{file_type}"
        new_file = f"{new_prefix}{file_type}"
        
        old_path = os.path.join(folder, old_file)
        new_path = os.path.join(folder, new_file)
        
        # İki dosya da mevcutsa karşılaştır
        if os.path.exists(old_path) and os.path.exists(new_path):
            print(f"Karşılaştırılıyor: {folder}/{old_file} <-> {folder}/{new_file}")
            
            # IP adreslerini okuyup ayır
            ips1 = set()
            ips2 = set()
            
            with open(old_path, 'r', encoding='utf-8') as f1:
                for line in f1:
                    if line.strip():
                        # Her satırı virgülle ayır ve her IP'yi temizle
                        for ip in line.strip().split(','):
                            clean_ip = ip.strip()
                            if clean_ip:
                                ips1.add(clean_ip)
                                
            with open(new_path, 'r', encoding='utf-8') as f2:
                for line in f2:
                    if line.strip():
                        # Her satırı virgülle ayır ve her IP'yi temizle
                        for ip in line.strip().split(','):
                            clean_ip = ip.strip()
                            if clean_ip:
                                ips2.add(clean_ip)

            # Karşılaştırmalar
            only_in_old = ips1 - ips2
            only_in_new = ips2 - ips1
            common_ips = ips1 & ips2  # Her iki dosyada da bulunan ortak IP'ler

            # Dosya tipini çıkarmak için (mixed, ips, ports)
            base_name = file_type.replace('.txt', '')
            
            # Karşılaştırma dosya adını oluştur
            comparison_file = f"{old_prefix}vs{new_prefix}{base_name}-comparison.txt"
            
            # OUTPUT KLASÖRÜNÜN KARŞILAŞTIRMALARI İÇİN VİRGÜLLE AYRILMIŞ FORMAT
            if folder == "output":
                output_compare_path = os.path.join("output-comparison", comparison_file)
                with open(output_compare_path, 'w', encoding='utf-8') as outfile:
                    outfile.write(f"# {old_file} içinde olup {new_file} içinde olmayanlar ({len(only_in_old)} IP):\n")
                    if only_in_old:
                        outfile.write(', '.join(sorted(only_in_old)))
                    else:
                        outfile.write("(Fark bulunamadı)")
                        
                    outfile.write(f"\n\n# {new_file} içinde olup {old_file} içinde olmayanlar ({len(only_in_new)} IP):\n")
                    if only_in_new:
                        outfile.write(', '.join(sorted(only_in_new)))
                    else:
                        outfile.write("(Fark bulunamadı)")
                    
                    # Her iki dosyada da bulunan ortak IP'ler
                    outfile.write(f"\n\n# Her iki dosyada da bulunan ortak IP'ler ({len(common_ips)} IP):\n")
                    if common_ips:
                        outfile.write(', '.join(sorted(common_ips)))
                    else:
                        outfile.write("(Ortak IP bulunamadı)")
            
            # RAW KLASÖRÜNÜN KARŞILAŞTIRMALARI İÇİN RAW FORMAT
            if folder == "raw":
                raw_compare_path = os.path.join("raw-comparison", comparison_file)
                with open(raw_compare_path, 'w', encoding='utf-8') as outfile:
                    # İlk bölüm: Eski dosyada olup yeni dosyada olmayanlar
                    outfile.write(f"# {old_file} içinde olup {new_file} içinde olmayanlar:\n")
                    for ip in sorted(only_in_old):
                        outfile.write(f"{ip}\n")
                    
                    # İkinci bölüm: Yeni dosyada olup eski dosyada olmayanlar
                    outfile.write(f"\n# {new_file} içinde olup {old_file} içinde olmayanlar:\n")
                    for ip in sorted(only_in_new):
                        outfile.write(f"{ip}\n")
                    
                    # Üçüncü bölüm: Her iki dosyada da bulunan ortak IP'ler
                    outfile.write(f"\n# Her iki dosyada da bulunan ortak IP'ler:\n")
                    for ip in sorted(common_ips):
                        outfile.write(f"{ip}\n")
        else:
            # Eğer dosyalar yoksa uyarı ver
            if not os.path.exists(old_path):
                print(f"Uyarı: {old_path} bulunamadı")
            if not os.path.exists(new_path):
                print(f"Uyarı: {new_path} bulunamadı")

print("\nKarşılaştırmalar tamamlandı.")
print("raw klasörü karşılaştırmaları: raw-comparison klasörüne yazıldı.")
print("output klasörü karşılaştırmaları: output-comparison klasörüne yazıldı.")
