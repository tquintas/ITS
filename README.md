# ITS
Intelligent Tutoring System for SIACUA

Variaveis gerais:
- tempo medio numa pergunta
- sucesso de uma pergunta
- sucesso de um conceito

Variaveis do aluno:
- tempo gasto numa pergunta
- numero de respostas certas por um conceito
- numero de respostas erradas por um conceito
- vetor temporal perguntas repondidas por conceito (all time e session) (historico)
- aceitação das decisoes do tutor

Ações:
- Muito tempo gasto num conceito + sucesso do conceitos < 0 = Scan
- Varias respostas erradas "consecutivas" + baixo belief nos conceitos vizinhos = Revisao
- Sucesso = 0 + Tendencia do aluno para aprofundar topicos = Aprofundar
- Belief muito baixo + poucas questoes respondidas = Aprender
- Belief isolado muito baixo num conceito + muitas questoes respondidas = Dificuldade num certo tópico
- Muito tempo gasto num conceito + muitas perguntas respondidas de sessão = Yoga break
- taxa média de sucesso num teste + taxa média geral das perguntas do teste = Verificação da performance

Variáveis do Tutor:
```c++
//Tempo que o aluno gasta, relativamente ao tempo médio, por conceito
double T_conceito = tempo_aluno_conceito / tempo_medio_conceito;
//Sucesso do aluno para um determinado conceito
double S_conceito = (certas_conceito - erradas_conceito) / respondidas_conceito;
//Tendencia para acertar
double Tc_conceito = 0;
int hSize = history_conceito.size();
for (int i = 0; i < hSize; --i)
{
    if (history_conceito[i]) Tc_conceito += 1 / pow(2, hSize - i);
}
//Tendencia para errar
double Te_conceito = 0;
int hSize = history_conceito.size();
for (int i = 0; i < hSize; --i)
{
    if (!history_conceito[i]) Te_conceito += 1 / pow(2, hSize - i);
}
//Performance
double performance = soma_percentagens_sucesso_aluno / soma_percentagens_sucesso_perguntas;
```

Sempre que uma questão é respondida, o tutor avalia as probabilidades do aluno necessitar uma das ações e devolve a ação que apresenta maior probabilidade

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
