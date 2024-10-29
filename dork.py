import requests
from bs4 import BeautifulSoup
import random
import re  # Düzenli ifadeler için
import time  # Gecikme eklemek için
from datetime import datetime  # Tarih ve saat için

# ANSI kaçış kodları (renkler)
LIGHT_BLUE = "\033[94m"
YELLOW = "\033[93m"
RESET = "\033[0m"

# Dork listesi ve açıklamaları
dork_list = {
    "inurl:login": "Login sayfalarını bulur.",
    "filetype:sql": "SQL dosyalarını bulur.",
    "intitle:index.of": "Dizin listelemelerini bulur.",
    "site:example.com": "Belirtilen siteye ait sonuçları bulur.",
    "filetype:pdf confidential": "PDF dosyalarında 'confidential' terimini arar.",
    "inurl:admin": "Yönetici panellerini bulur.",
    "intitle:\"Admin Login\"": "\"Admin Login\" başlığına sahip sayfaları bulur.",
    "intext:\"username\" filetype:log": "Log dosyalarında 'username' terimini arar.",
    "inurl:phpmyadmin": "phpMyAdmin arayüzlerini bulur.",
    "filetype:xls password": "Excel dosyalarında 'password' terimini arar.",
    "inurl:config.php": "PHP yapılandırma dosyalarını bulur.",
    "intext:\"email\" filetype:xls": "Excel dosyalarında e-posta adreslerini bulur."
}

search_history = []

def google_search(dork, num_results=10, num_pages=3):
    dork_encoded = requests.utils.quote(dork)
    results = []
    
    for page in range(num_pages):
        start = page * 10  # Her sayfada 10 sonuç var
        search_url = f"https://www.google.com/search?q={dork_encoded}&start={start}&num=10"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
        }
        
        try:
            response = requests.get(search_url, headers=headers)
            response.raise_for_status()  # Hata kontrolü
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Arama sonuçlarının bulunduğu elementleri belirleme
            for item in soup.find_all('h3'):
                link = item.find_parent('a')['href']
                results.append(link)

            time.sleep(2)  # Google'ın engel koymaması için bekleme süresi
        
        except Exception as e:
            print(f"Arama yapılırken bir hata oluştu: {e}")
            return []
    
    # Tekrarlayan sonuçları kaldır
    unique_results = list(set(results))
    
    return unique_results[:num_results]

def print_dork_list():
    print("Dork Listesi:")
    for dork, description in dork_list.items():
        print(f"{dork}: {description}")

def clean_filename(filename):
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

def save_results(results, dork):
    cleaned_dork = clean_filename(dork)
    # Bugünün tarihini al ve dosya adı için formatla
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"results_{cleaned_dork}_{date_str}.txt"
    
    with open(filename, 'w') as f:
        for result in results:
            f.write(result + '\n')
    print(f"Sonuçlar '{filename}' dosyasına kaydedildi.")

def show_history():
    print("Arama Geçmişi:")
    for index, entry in enumerate(search_history):
        print(f"{index + 1}: {entry}")

def welcome_message():
    ascii_art = f"""
{LIGHT_BLUE}                   ###                 ##
                    ##                 ##
  #####    ####     ##  ##  ##  ##    #####    ####
 ##           ##    ## ##   ##  ##     ##         ##
  #####    #####    ####    ##  ##     ##      #####
      ##  ##  ##    ## ##   ##  ##     ## ##  ##  ##
 ######    #####    ##  ##   ######     ###    #####
{RESET}
         Welcome to Dork  Scanner Tool! 
    """
    print(ascii_art)

def show_creator():
    print("Yapımcı: Bloodysword\n İnstagram bloodysword.666")

def main():
    welcome_message()
    
    while True:
        print(YELLOW + "\nMenü:" + RESET)
        print(YELLOW + "1. Dork Tarama" + RESET)
        print(YELLOW + "2. Dork Listele" + RESET)
        print(YELLOW + "3. Arama Geçmişi Göster" + RESET)
        print(YELLOW + "4. Rastgele Dork Tarama" + RESET)
        print(YELLOW + "5. Yapımcı" + RESET)
        print(YELLOW + "6. Çıkış" + RESET)

        choice = input("Seçiminizi yapın (1-6): ").strip()
        
        if choice == '1':
            dork = input("Dork'unuzu girin: ")
            results = google_search(dork)
            print("Bulunan siteler:")
            if results:
                for index, site in enumerate(results):
                    print(f"{index + 1}: {site}")
            else:
                print("Sonuç bulunamadı.")
            save_option = input("Sonuçları kaydetmek ister misiniz? (e/h): ").lower()
            if save_option == 'e':
                save_results(results, dork)
            search_history.append(dork)
        
        elif choice == '2':
            print_dork_list()
        
        elif choice == '3':
            show_history()
        
        elif choice == '4':
            dork = random.choice(list(dork_list.keys()))
            print(f"Seçilen Dork: {dork}")
            results = google_search(dork)
            print("Bulunan siteler:")
            if results:
                for index, site in enumerate(results):
                    print(f"{index + 1}: {site}")
            else:
                print("Sonuç bulunamadı.")
            save_option = input("Sonuçları kaydetmek ister misiniz? (e/h): ").lower()
            if save_option == 'e':
                save_results(results, dork)
            search_history.append(dork)

        elif choice == '5':
            show_creator()
        
        elif choice == '6':
            print("Çıkılıyor...")
            break
        
        else:
            print("Geçersiz seçim, lütfen tekrar deneyin.")

if __name__ == "__main__":
    main()
