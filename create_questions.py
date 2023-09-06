import random2 as rd
import time as _t

def QuestionLevel(level):
    a = round(5 * (2*rd.random() - 1), level-1)
    b = round(5 * (2*rd.random() - 1), level-1)
    sign = round(rd.random())
    r = round(a + b*(-1)**sign, level-1)
    ans = [r]
    while len(ans) < 4:
        e = round(r + (6-level)*(2*rd.random() - 1)*(-1)**sign, level-1)
        if e not in ans: ans.append(e)
    rd.shuffle(ans)
    m = f"[Level: {level}] {a} {'-' if sign else '+'} {f'({b})' if b < 0 else b} = ?\n(a) {ans[0]}\n(b) {ans[1]}\n(c) {ans[2]}\n(d) {ans[3]}"
    print(m)
    return ans.index(r)

def AnswerQuestion(level):
    r = QuestionLevel(level)
    print(r)
    letters = ["a", "b", "c", "d"]
    t1 = _t.time()
    while True:
        ans = str(input("Answer: "))
        if ans not in letters:
            print("Invalid answer. Try again.")
            continue
        else:
            ans = letters.index(ans)
            break
    time = _t.time() - t1
    return r == ans , time

def SaveResultsToBD(level_list, missed, bs):
    with open("results.txt", "w+") as f:
        f.write(str(len(level_list))+";")
        f.write(str(level_list)+";")
        f.write(str(missed)+";")
        f.write(str(bs)+"\n")

def LoadResultsFromBD(n):
    level_list = []
    missed = []
    bs = []
    with open("results.txt", "r") as f:
        lines = f.readlines()
        for line in lines:
            contents = line.strip().split(";")
            if int(contents[0]) == n:
                level_list.append(contents[1].strip("][").split(", "))
                missed.append(contents[2].strip("][").split(", "))
                bs.append(contents[3].strip("][").split(", "))
    return level_list, missed, bs

def SaveTutorVars(user, topic, logs, logs_session, ):
    with open("tutor_vars.txt", "w+") as f:
        pass

def TutorDecisions():
    
    #verifica se a media dos tempos está no intervalo de confiança a 95%
    #verifica se o sucesso é baixo
    #verifica se o aluno respondeu a muitas ou poucas questões (da sessao ou total)
    #verifica se o belief é baixo e se o belief dos pais também é baixo
    #verifica se a tendência é alta
    #utilizar os diferentes valores num modelo estatistico para determinar qual decisão tem maior likelyhood de acontecer
    pass

def StartTest(b, n_questions = 10):
    level = 1
    level_list = []
    missed = []
    bs = []
    times = []
    N = 1
    while N <= n_questions:
        print(f"Question {N}:")
        right, time = AnswerQuestion(level)
        times.append(time)
        missed.append(not right)
        level_list.append(level)
        bs.append(b)
        try:
            if missed[-1]:
                b -= 0.05
                if b < 0: b = 0
                print("Wrong!")
                if level == 5 or (level_list[-2] == level and missed[-2]) or level_list[-2] != level:
                    if level != 1:
                        print("Level down...")
                        level -= 1
            else:
                b += 0.05
                if b > 1: b = 1
                print("Correct!")
                if level != 5 and (level_list[-2] == level and not missed[-2] and not missed[-3]) or (level_list[-2] == level and level_list[-2] != level_list[-3] and  not missed[-2] and not missed[-3]):
                    print("Level up!")
                    level += 1
        except:
            pass
        TutorDecisions()
        N += 1
        print("\n")
    mean_time = sum(times)/len(times)
    print(f"Your mean time was {mean_time} seconds.")
    TutorDecisions()
    return level_list, missed, bs