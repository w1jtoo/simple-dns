from src.dnsserver import start_server 

def main():
    start_server("127.0.0.1", 1155, [("192.168.1.1", 53)])

if __name__ == "__main__":
    main()
