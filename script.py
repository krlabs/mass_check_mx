import dns.resolver

# Функція для отримання MX-записів
def get_mx_records(domain):
    try:
        # Спроба використати новий метод 'resolve'
        try:
            mx_records = dns.resolver.resolve(domain, 'MX')
        except AttributeError:
            # Якщо виникає помилка, використовуємо старий метод 'query'
            mx_records = dns.resolver.query(domain, 'MX')
        return [(r.exchange.to_text(), r.preference) for r in mx_records]
    except Exception as e:
        return f"Error: {e}"

# Читання доменів із файлу
def read_domains(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

# Запис результатів у файл
def write_results(results, output_file):
    with open(output_file, 'w') as file:
        for domain, mx in results.items():
            if isinstance(mx, str):  # Якщо виникла помилка
                file.write(f"{domain}: {mx}\n")
            else:
                for record in mx:
                    file.write(f"{domain}: {record[0]} (Preference: {record[1]})\n")

# Основна функція
def main(input_file, output_file):
    domains = read_domains(input_file)
    results = {domain: get_mx_records(domain) for domain in domains}
    write_results(results, output_file)
    print(f"MX-записи збережено в {output_file}")

if __name__ == "__main__":
    input_file = 'domains.txt'  # Введіть шлях до файлу зі списком доменів
    output_file = 'mx_records.txt'  # Введіть шлях для збереження результатів
    main(input_file, output_file)
