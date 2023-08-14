# ITS
Intelligent Tutoring System for SIACUA

Variaveis gerais:
- tempo medio numa pergunta
- taxa de sucesso de uma pergunta

Variaveis do aluno:
- tempo gasto numa pergunta
- numero de respostas certas para um conceito
- numero de respostas erradas para um conceito

Ações:
- Muito tempo gasto num conceito + sucesso do conceitos < 0 = Scan
- Varias respostas erradas consecutivas + baixo belief nos conceitos vizinhos = Revisao
- Sucesso = 0 + Tendencia do aluno para aprofundar topicos = Aprofundar
- Belief muito baixo + poucas questoes respondidas = Aprender
- 

Cada teste constitui perguntas de nivel 1 até nivel 5. Assim que uma questão de nível 5 for respondida corretamente, o teste acaba. Quando todas as perguntas forem respondidas, o progresso fica a 100%. Um teste pode ter questões repetidas, desde que respeitem os níveis de dificuldade e que não tenham sido respondidas há pouco tempo. Um teste não pode ter mais de 20 (?) perguntas e o utilizador pode sair e entrar em qualquer altura do teste, sem perder o progresso.
- acertar 3 perguntas consecutivas no mesmo nível = subir de nível
- acertar 2 perguntas consecutivas aquando da mudança de nível = subir de nível
- falhar a primeira pergunta aquando da mudança de nível = descida de nível
- falhar 2 perguntas consecutivas no mesmo nível = descer de nível
Código das perguntas:
```c++
int nivel_anterior = 1;
int nivel_atual = 1;
int respondido = 0;
std::vector<bool> certas(20);
while (respondido <= 20)
{
    MostrarQuestao(nivel_atual);
    bool acertou = ResponderQuestao();
    certas[respondido] = acertou;
    try
    {
        if (acertou)
        {
            if (nivel_atual == 5)
            {
                TerminarTeste();
                break;
            }
            else if ((nivel_anterior == nivel_atual && certas[respondido - 1] && certas[respondido - 2]) || (nivel_anterior != nivel_atual && certas[respondido - 1]))
            {
                nivel_anterior = nivel_atual;
                nivel_atual++;
            }
            else
            {
                nivel_anterior = nivel_atual;
            }
        }
        else
        {
            if ((nivel_atual == 5) || (nivel_anterior == nivel_atual && !certas[respondido - 1]) || (nivel_anterior != nivel_atual))
            {
                if (nivel_atual == 1)
                {
                    TerminarTeste();
                    break;
                }
                else
                {
                    nivel_anterior = nivel_atual;
                    nivel_atual--;
                }
            }
            else
            {
                nivel_anterior = nivel_atual;
            }
        }
    }
    catch
    {
        //caso seja a primeira pergunta
    }
    DecisoesTutor();
    respondido++;
}
```
