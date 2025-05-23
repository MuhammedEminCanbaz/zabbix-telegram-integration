# Zabbix + Telegram Entegrasyonu

Bu proje, Zabbix sistem izleme aracının Telegram bot ile entegre edilerek olay (trigger) bazlı anlık bildirim gönderebilmesini sağlamaktadır. Amaç, sistem yöneticisinin kritik olayları doğrudan mesaj yoluyla öğrenmesini sağlayarak müdahale süresini kısaltmak ve sistem güvenliğini artırmaktır.

## Kullanılan Teknolojiler

- Zabbix Server 6.0+
- Ubuntu 22.04
- MySQL (veritabanı)
- Apache + PHP (Zabbix frontend)
- Zabbix Agent
- Telegram Bot API
- Python 3 (requests modülü)

## Zabbix Kurulumu

### 1. Repo ve Paket Kurulumu
```bash
wget https://repo.zabbix.com/zabbix/6.0/ubuntu/pool/main/z/zabbix-release/zabbix-release_6.0-1+ubuntu22.04_all.deb
sudo dpkg -i zabbix-release_6.0-1+ubuntu22.04_all.deb
sudo apt update
sudo apt install zabbix-server-mysql zabbix-frontend-php zabbix-apache-conf zabbix-sql-scripts zabbix-agent mysql-server

## Veritabanı Yapılandırması

-sudo mysql
-create database zabbix character set utf8mb4 collate utf8mb4_bin;
-create user zabbix@localhost identified by 'zabbixpass';
-grant all privileges on zabbix.* to zabbix@localhost;
-quit;

### Zabbix Veritabanı Şemasının Aktarılması

-zcat /usr/share/zabbix-sql-scripts/mysql/server.sql.gz | mysql -uzabbix -p zabbix

### Yapılandırma ve Servis Başlatma

-sudo nano /etc/zabbix/zabbix_server.conf
# DBPassword=zabbixpass satırı eklenir
-sudo systemctl restart zabbix-server zabbix-agent apache2
-sudo systemctl enable zabbix-server zabbix-agent apache2

##Tarayıcıdan http://localhost/zabbix adresine giderek web kurulum sihirbazı tamamlanır.

## Telegram Bot Oluşturma

-@BotFather kullanılarak yeni bot oluşturuldu

-Token alındı

-@userinfobot ile kullanıcı chat_id değeri öğrenildi

### Python Bildirim Scripti

/scripts/telegram.py konumunda oluşturuldu

-python3 scripts/telegram.py 123456789 "Test" "Zabbix Telegram testi başarılı" test edildi

## Zabbix Üzerinde Tanımlamalar
Media Type
Name: TelegramScript

Type: Script

Script name: telegram.py

Parameters:

{ALERT.SENDTO}

{ALERT.SUBJECT}

{ALERT.MESSAGE}

### Kullanıcıya Medya Eklenmesi
Send to: chat_id

Active: 1-7,00:00-24:00 (24x7)

Severity: All

Type: TelegramScript

### Action Tanımı
Name: TelegramScript Test Action

Event source: Triggers

Operation:

Send message to Admin

Send only to: TelegramScript

Custom message: ✅

Subject: {TRIGGER.NAME}

Message: {TRIGGER.STATUS}: {TRIGGER.NAME} on {HOST.NAME}

Test Trigger
Zabbix sunucusuna item eklenmiştir:

Key: system.cpu.load[percpu,avg1]

Update interval: 30s

### {Zabbix server:system.cpu.load[percpu,avg1].last()}>0.001 ifadesi ile anomalinin sık gerçekleşmesi sağlandı

# Sonuç
Zabbix sisteminde oluşan olaylar başarıyla Telegram'a aktarılmıştır. Telegram bot entegrasyonu ile kullanıcıya anında mesaj gönderimi sağlanarak sistem izleme süreci daha güvenilir ve hızlı hale getirilmiştir.
