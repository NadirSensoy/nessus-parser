import os
import re

def get_available_filename(directory, filename):
    """
    Eğer filename mevcutsa, 'filename(1)', 'filename(2)' şeklinde isimlendirerek
    yeni bir dosya adı üretir.
    """
    base, ext = os.path.splitext(filename)
    counter = 1
    candidate = os.path.join(directory, filename)
    while os.path.exists(candidate):
        candidate = os.path.join(directory, f"{base}({counter}){ext}")
        counter += 1
    return candidate

# Klasörleri oluştur
os.makedirs('raw', exist_ok=True)
os.makedirs('output', exist_ok=True)

try:
    # input.txt'den satırları oku
    with open('input.txt', 'r', encoding='utf-8') as infile:
        lines = infile.readlines()

    # Kullanıcıdan bir önek iste (zorunlu)
    while True:
        output_prefix = input("Çıktı dosyalarının öneki (zorunlu): ").strip()
        if not output_prefix:
            print("Hata: Önek boş olamaz! Lütfen bir önek girin.")
            continue
        break

    # Önek tire ile bitmiyorsa ekle
    if not output_prefix.endswith('-'):
        output_prefix += '-'

    # IP adreslerini filtrele (port olmadan da çalışacak)
    filtered_lines = []
    ip_port_dict = {}  # IP ve port bilgilerini ayrı saklayacağız
    
    for line in lines:
        # İlk format: IP (tcp|udp)/port[/service] formatı
        match = re.match(r'(\d+\.\d+\.\d+\.\d+)\s*\((tcp|udp)/(\d+)(?:/\w+)?', line)
        if match:
            ip = match.group(1)
            port = match.group(3)
            ip_port_dict[ip] = port
            filtered_lines.append(f"{ip}:{port}")
            continue
        
        # İkinci format: IP:port formatı
        match = re.match(r'(\d+\.\d+\.\d+\.\d+):(\d+)', line)
        if match:
            ip = match.group(1)
            port = match.group(2)
            ip_port_dict[ip] = port
            filtered_lines.append(f"{ip}:{port}")
            continue
        
        # Sadece IP formatı - port belirtmiyoruz
        match = re.match(r'^\s*(\d+\.\d+\.\d+\.\d+)\s*$', line)
        if match:
            ip = match.group(1)
            ip_port_dict[ip] = ""  # Port yok
            filtered_lines.append(ip)  # Sadece IP
            continue
            
        # Üçüncü format: Virgülle ayrılmış IP:port veya sadece IP listesi
        if ',' in line:
            parts = [p.strip() for p in line.split(',') if p.strip()]
            for part in parts:
                # IP:port formatı
                match = re.match(r'(\d+\.\d+\.\d+\.\d+):(\d+)', part)
                if match:
                    ip = match.group(1)
                    port = match.group(2)
                    ip_port_dict[ip] = port
                    filtered_lines.append(f"{ip}:{port}")
                    continue
                    
                # Sadece IP formatı
                match = re.match(r'(\d+\.\d+\.\d+\.\d+)', part)
                if match:
                    ip = match.group(1)
                    ip_port_dict[ip] = ""  # Port yok
                    filtered_lines.append(ip)  # Sadece IP

    # Boş satırları filtrele
    non_empty_lines = [line for line in filtered_lines if line.strip()]
    
    # Eşsiz değerleri al ve sırala
    unique_mixed_lines = list(set(non_empty_lines))
    # IP adreslerine göre sırala
    sorted_mixed_lines = sorted(unique_mixed_lines, key=lambda x: [int(part) for part in x.split(':')[0].split('.')])

    # Öneki dosya adlarına uygula
    mixed_filename = f"{output_prefix}mixed.txt"
    ips_filename = f"{output_prefix}ips.txt"
    ports_filename = f"{output_prefix}ports.txt"

    # Dosya adlarını kontrol ederek oluştur
    mixed_raw_path = get_available_filename('raw', mixed_filename)
    ips_raw_path = get_available_filename('raw', ips_filename)
    ports_raw_path = get_available_filename('raw', ports_filename)
    mixed_out_path = get_available_filename('output', mixed_filename)
    ips_out_path = get_available_filename('output', ips_filename)
    ports_out_path = get_available_filename('output', ports_filename)

    # raw/mixed.txt yaz - eşsiz değerlerle
    with open(mixed_raw_path, 'w', encoding='utf-8') as mixedfile:
        mixedfile.writelines(line + '\n' for line in sorted_mixed_lines)

    # IP ve portları ayır
    ips = []
    ports = set()

    for ip, port in ip_port_dict.items():
        ips.append(ip)
        if port:  # Sadece boş olmayan portları ekle
            ports.add(port)

    # Benzersiz IP'leri bul
    unique_ips = list(set(ips))
    sorted_ips = sorted(unique_ips, key=lambda ip: [int(octet) for octet in ip.split('.')])
    sorted_ports = sorted(ports, key=int)

    # raw/ips.txt ve ports.txt yaz
    with open(ips_raw_path, 'w', encoding='utf-8') as ipsfile:
        ipsfile.writelines(ip + '\n' for ip in sorted_ips)

    with open(ports_raw_path, 'w', encoding='utf-8') as portsfile:
        portsfile.writelines(port + '\n' for port in sorted_ports)

    # output/*.txt dosyalarına virgülle ayırarak yaz
    with open(ips_out_path, 'w', encoding='utf-8') as ipsfile:
        ipsfile.write(', '.join(sorted_ips))

    with open(ports_out_path, 'w', encoding='utf-8') as portsfile:
        portsfile.write(', '.join(sorted_ports))

    with open(mixed_out_path, 'w', encoding='utf-8') as mixedfile:
        mixedfile.write(', '.join(sorted_mixed_lines))

    print(f"İşlem tamamlandı. Dosyalar '{output_prefix}' öneki ile kaydedildi.")

except FileNotFoundError:
    print("Hata: input.txt dosyası bulunamadı.")
except Exception as e:
    print(f"Hata oluştu: {e}")
