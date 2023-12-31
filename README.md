# ITS
Intelligent Tutoring System for SIACUA

Variaveis gerais:
- tempo medio numa pergunta
- sucesso de uma pergunta
- sucesso de um conceito

Variaveis do aluno:
- tempo gasto numa pergunta
- numero de respostas certas por um conceito
- vetor temporal perguntas repondidas por conceito (all time e session) (historico)
- aceitação das decisoes do tutor

Ações:
- Muito tempo gasto num conceito + sucesso do conceitos < 0.5 = Scan
- Varias respostas erradas "consecutivas" + baixo belief nos conceitos vizinhos = Revisao
- Sucesso = 0.5 + Tendencia do aluno para aprofundar topicos = Aprofundar
- Belief muito baixo + poucas questoes respondidas = Aprender
- Belief isolado muito baixo num conceito + muitas questoes respondidas = Dificuldade num certo tópico
- Muito tempo gasto num conceito + muitas perguntas respondidas de sessão = Yoga break

Variáveis do Tutor:
```c++
//Tempo que o aluno gasta, relativamente ao tempo médio, por conceito
double T_conceito = tempo_aluno_conceito / tempo_medio_conceito;
//Sucesso do aluno para um determinado conceito
double S_conceito = certas_conceito / respondidas_conceito;
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
```

A tendencia é guardada apenas como um número e em vez de ser calculada a partir de um vetor, é guardado o número na base de dados e sempre que o aluno responde a uma questão, é feito:
```c++
tendencia_errar = (tendencia_errar + (errou ? 1 : 0)) / 2
```
Assim, apenas é necessário guardar um número na base de dados, por conceito. Para atualizar o tempo por conceito, é usado o código (antes de adicionar a resposta à variavel `` respostas_conceito ``):
```c++
tempo_medio *= (respostas_conceito + (tempo_observado / tempo_medio)) / (respostas_conceito + 1);
tempo_medio2 *= (respostas_conceito + (tempo_observado * tempo_observado / tempo_medio2)) / (respostas_conceito + 1);
tempo_var = tempo_medio2 - (tempo_medio * tempo_medio);
```

A base de dados do tutor, entao, tem de ter a seguinte estrutura:
| ID | UserId | Topic | Logs_Total | Logs_Session | Success_Total | Success_Session | Tendency | Time_Mean | Time_Mean2 | Time_Var | Belief |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 21 | Cp02_Algebra | 34 | 9 | 18 | 7 | 0.43781112314900383 | 63.41351616413721 | 5266.390409754405 | 1245.1163774551137 | 0.43 |


---

Tendo 5 dificuldades, seja:

$$ {\boldsymbol \beta} =
\begin{bmatrix}
    \text{Beta}\left(\alpha_1, 1 - \alpha_1\right) \\
    \text{Beta}\left(\alpha_2, 1 - \alpha_2\right) \\
    \text{Beta}\left(\alpha_3, 1 - \alpha_3\right) \\
    \text{Beta}\left(\alpha_4, 1 - \alpha_4\right) \\
    \text{Beta}\left(\alpha_5, 1 - \alpha_5\right)
\end{bmatrix}    
$$

Onde $\alpha_i$ é o sucesso de uma questão de dificuldade $i$.

$$ L({\bf Q}, {\bf b}, {\bf v}) = \prod^N_n {\mathcal B}\left( \left({\bf Q}_n \cdot {\boldsymbol \beta} \right) (1 - {\bf b}_n), {\bf v}_n \right) $$

O _mixture model_ é:

$$ \sum^K_k \rho_k \prod^N_n {\mathcal B}\left( \left({\bf Q}_n \cdot {\boldsymbol \beta}_k \right) (1 - {\bf b}_n), {\bf v}_n \right) $$

Para ${\bf Q}^s, {\bf p}^s, {\bf v}^s$ onde $s$ representa um aluno, para um número $K$ de componentes tem-se que:

$$ L_{s,k} \leftarrow \rho_k \prod^N_{n=1} {\mathcal B}\left( \left({\bf Q}^s_n \cdot {\boldsymbol \beta}_k \right) (1 - {\bf b}^s_n), {\bf v}^s_n \right) $$

$$ z_{s,k} \leftarrow \frac{L_{s,k}}{\sum_{k'}L_{s,k'}} $$

---

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
