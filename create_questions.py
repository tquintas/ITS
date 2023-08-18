from learning_curve import *

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
    while True:
        ans = str(input("Answer: "))
        if ans not in letters:
            print("Invalid answer. Try again.")
            continue
        else:
            ans = letters.index(ans)
            break
    return r == ans

def SaveToBD(level_list, missed, bs):
    with open("results.txt", "w+") as f:
        f.write(len(level_list)+";")
        f.write(str(level_list)+";")
        f.write(str(missed)+";")
        f.write(str(bs)+"\n")

def LoadFromBD(n):
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

def Stats(n):
    g = 0.25
    s = 0.05
    groups = 3
    level_list, missed, bs = LoadFromBD(n)
    p, q = EM([level_list], [bs], s, g, groups, [missed], 1, 1, 15)
    ploting(groups, len(level_list[0]), p, q)

def StartTest(b, max_questions = 20):
    level = 1
    level_list = []
    missed = []
    bs = []
    N = 0
    while N < max_questions:
        missed.append(not AnswerQuestion(level))
        level_list.append(level)
        bs.append(b)
        try:
            if missed[-1]:
                b -= 0.05
                if b < 0: b = 0
                print("Wrong!")
                if level == 5 or (level_list[-2] == level and missed[-2]) or level_list[-2] != level:
                    if level == 1:
                        print("Test failed!")
                        break
                    else:
                        print("Level down...")
                        level -= 1
            else:
                b += 0.05
                if b > 1: b = 1
                print("Correct!")
                if level == 5:
                    print("Test completed!")
                    break
                elif (level_list[-2] == level and not missed[-2] and not missed[-3]) or (level_list[-2] == level and level_list[-2] != level_list[-3] and  not missed[-2] and not missed[-3]):
                    print("Level up!")
                    level += 1
        except:
            pass
        #TutorDecisions()
        N += 1
        print("\n")
    SaveToBD(level_list, missed, bs)
    Stats(len(level_list))