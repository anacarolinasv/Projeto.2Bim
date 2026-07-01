"""Cores ANSI para o terminal TaskFlow."""


class C:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"

    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"

    @staticmethod
    def wrap(texto, *codes):
        return "".join(codes) + str(texto) + C.RESET

    @staticmethod
    def banner():
        return (
            f"{C.CYAN}{C.BOLD}"
            "\n  ╔══════════════════════════╗"
            "\n  ║        TaskFlow          ║"
            "\n  ╚══════════════════════════╝"
            f"{C.RESET}"
        )

    @staticmethod
    def menu_titulo(texto):
        return C.wrap(f"\n=== {texto} ===", C.BLUE, C.BOLD)

    @staticmethod
    def opcao(num, texto):
        return f"{C.wrap(num, C.CYAN, C.BOLD)} - {texto}"

    @staticmethod
    def opcoes(*pares):
        return "   ".join(C.opcao(n, t) for n, t in pares)

    @staticmethod
    def opcao_sair(texto="Sair / Voltar"):
        return C.opcao(0, texto)

    @staticmethod
    def prompt(texto):
        return C.wrap(texto, C.YELLOW)

    @staticmethod
    def sucesso(texto):
        return C.wrap(f"✓ {texto}", C.GREEN, C.BOLD)

    @staticmethod
    def erro(texto):
        return C.wrap(f"✗ {texto}", C.RED)

    @staticmethod
    def info(texto):
        return C.wrap(texto, C.DIM)

    @staticmethod
    def aviso(texto):
        return C.wrap(f"! {texto}", C.YELLOW)

    @staticmethod
    def destaque(texto):
        return C.wrap(texto, C.MAGENTA, C.BOLD)

    @staticmethod
    def secao(texto):
        return C.wrap(f"-- {texto} --", C.BLUE)

    @staticmethod
    def item(texto):
        return C.wrap(f"  • {texto}", C.WHITE)
