import argparse
import sys
from src.forward import proxy_forward
from src.proxy import list_proxy_web
from src.banner import banner, info
from src.helpers import identify

def main():
    banner()
    info()
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--download", action="store_true", help="Download list proxies")
    parser.add_argument("--ip", help="IP do proxy local")
    parser.add_argument("--timeout", default=10, help="Timeout proxy local")
    parser.add_argument("--port", help="Porta do proxy local")
    args = parser.parse_args()

    if args.download:
        print("- [x] Iniciando o download da lista de proxy!")
        proxy_list = list_proxy_web()
        if proxy_list:
            print("- [x] Lista de proxies baixada com sucesso \o/")
            print(f'- [x] Quantidade de ips disponíveis: {len(proxy_list)} ')

    if args.ip and args.port:
        identify_list = identify()
        if identify_list:
            print(f"- [x] Iniciando proxy forward na porta {args.port} com IP {args.ip}")
            proxy_forward(int(args.port), args.ip, int(args.timeout))
        else:
            print(f"- [x] Realize o download da lista para que possa utilizar a ferramenta!")
    sys.exit(1)


if __name__ == "__main__":
  try:
    main()
    print('[x] - Processo finalizado, espero ter ajuda-lo.')
    sys.exit(1)
  except KeyboardInterrupt:
    print("\nOperação interrompida pelo usuário.")
    sys.exit(0)

