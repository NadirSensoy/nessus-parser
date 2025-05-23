1- input.txt'ye Nessus çıktısından alınan kısmı yapıştırıyoruz.

2- run.bat dosyasına tıklıyoruz veya script.py'ı terminalden çalıştırıyoruz.
   - Çıktı dosyalarının öneki sorulacaktır (örn. "proje1", "scan-2025")
   - Önek olmadan çalıştırmak için Enter tuşuna basabilirsiniz
   - v3.0 her çalıştırıldığında üzerine yazmak yerine yeni dosya oluşturuyor (mixed.txt, mixed(1).txt, vb.)

3- Desteklenen Giriş Formatları:
   - IP (tcp|udp)/port[/service] formatı: 23.88.53.46 (tcp/443/www)
   - IP:port formatı: 10.10.2.25:5666
   - Virgülle ayrılmış IP:port listesi: 10.10.2.25:5666, 10.10.4.107:5666, ...
   - Sadece IP formatı: 10.10.2.25
   - Virgülle ayrılmış IP listesi: 10.10.2.25, 10.10.4.107, ...
   - Çok satırlı liste (Aynı satırda veya farklı satırlarda yukarıdaki formatlar kullanılabilir)

4- Oluşturulan dosyalar:
   - raw/ klasörü: Her satırda bir IP:port bilgisi
     * mixed.txt: Tüm IP:port eşleşmeleri (benzersiz)
     * ips.txt: Sadece benzersiz IP adresleri 
     * ports.txt: Sadece benzersiz port numaraları
   
   - output/ klasörü: Virgülle ayrılmış formatta
     * mixed.txt: Tüm IP:port eşleşmeleri (benzersiz)
     * ips.txt: Sadece benzersiz IP adresleri
     * ports.txt: Sadece benzersiz port numaraları

5- Karşılaştırma özelliği:
   - compare_versions.py dosyasını çalıştırarak farklı önekli dosyaları karşılaştırabilirsiniz
   - Daha önce script.py ile oluşturduğunuz dosyaların önekleri otomatik olarak listelenecektir
   - Listelenen öneklerden birini numara (#) yazarak veya doğrudan adını yazarak seçebilirsiniz:
     * İlk soruda ESKİ dosya öneki seçilmelidir
     * İkinci soruda YENİ dosya öneki seçilmelidir
   - Sonuçlar iki farklı klasörde oluşturulur:
     * raw-comparison/: Her satırda bir IP formatında
     * output-comparison/: Virgülle ayrılmış formatta
   - Her karşılaştırma dosyasında:
     * İlk dosyada olup ikinci dosyada olmayan IP'ler
     * İkinci dosyada olup ilk dosyada olmayan IP'ler
     * Her iki dosyada da bulunan ortak IP'ler

6- clean.bat dosyasını çalıştırarak input.txt'nin içeriğini ve tüm oluşturulan klasörleri (raw, output, raw-comparison, output-comparison) temizleyebilirsiniz.

Örnek çıktılar:

raw/mixed.txt örneği:
192.168.1.1:80
192.168.1.2:443
192.168.1.3:22
192.168.1.4

raw/ips.txt örneği:
192.168.1.1
192.168.1.2
192.168.1.3
192.168.1.4

raw/ports.txt örneği:
22
80
443

output/mixed.txt örneği:
192.168.1.1:80, 192.168.1.2:443, 192.168.1.3:22, 192.168.1.4

output/ips.txt örneği:
192.168.1.1, 192.168.1.2, 192.168.1.3, 192.168.1.4

output/ports.txt örneği:
22, 80, 443

raw-comparison/eski-vs-yeni-mixed-comparison.txt örneği:
# eski-mixed.txt içinde olup yeni-mixed.txt içinde olmayanlar:
192.168.1.1:80
192.168.1.5:21

# yeni-mixed.txt içinde olup eski-mixed.txt içinde olmayanlar:
192.168.1.4:8080

# Her iki dosyada da bulunan ortak IP'ler:
192.168.1.2:443
192.168.1.3:22

output-comparison/eski-vs-yeni-mixed-comparison.txt örneği:
# eski-mixed.txt içinde olup yeni-mixed.txt içinde olmayanlar (2 IP):
192.168.1.1:80, 192.168.1.5:21

# yeni-mixed.txt içinde olup eski-mixed.txt içinde olmayanlar (1 IP):
192.168.1.4:8080

# Her iki dosyada da bulunan ortak IP'ler (2 IP):
192.168.1.2:443, 192.168.1.3:22

Hayırlı raporlamalar - by revivalist :()
