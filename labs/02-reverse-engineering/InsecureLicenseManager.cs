using System;

namespace GuardAI.Labs
{
    /// <summary>
    /// VULNERABILIDADE: CWE-798 (Use of Hardcoded Credentials)
    /// Em compilacoes .NET (CIL) ou binarios nativos, strings e constantes
    /// ficam gravadas em texto puro ou facilmente recuperaveis por descompiladores.
    /// </summary>
    public class InsecureLicenseManager
    {
        // Segredo gravado estaticamente no binario compilado
        private const string MASTER_SECRET_KEY = "GUARD-AI-ENTERPRISE-2026-TOKEN";

        public static bool ValidateKey(string key)
        {
            if (string.IsNullOrEmpty(key)) return false;
            return key == MASTER_SECRET_KEY;
        }

        public static void Main(string[] args)
        {
            Console.WriteLine("=== Validador de Licenca Corporativa ===");
            Console.Write("Digite sua chave de ativacao: ");
            string inputKey = Console.ReadLine();

            if (ValidateKey(inputKey))
            {
                Console.WriteLine("[+] Licenca valida! Acesso concedido aos recursos confidenciais.");
            }
            else
            {
                Console.WriteLine("[-] Chave incorreta! Acesso negado.");
            }
        }
    }
}
