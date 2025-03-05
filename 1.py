import random
import time
import os
import requests  # 用于云验证

def red(text):
    return '\033[31m' + str(text) + '\033[0m'

def blue(text):
    return '\033[34m' + str(text) + '\033[0m'  

def green(text):
    return '\033[32m' + str(text) + '\033[0m'

USER_DIR = os.path.expanduser("~")
RECORD_PATH = os.path.join(USER_DIR, "record.txt")
VERIFIED_KEY_PATH = os.path.join(USER_DIR, "verified_key.txt")

# 云端卡密存储地址（你需要自己托管这个文件）
KEYS_URL = "https://gist.githubusercontent.com/wuyan1337/39f38cc902260581151393ac143b04d3/raw/c4d1585b3a95126b7308fda2d10b58799cd80378/gistfile1.txt"

def load_record():
    if os.path.exists(RECORD_PATH):
        with open(RECORD_PATH, "r") as file:
            data = file.read().split(',')
            return float(data[0]), int(data[1]), float(data[2])
    return 0.0, 0, 0.0

def save_record(new_time, new_questions, new_accuracy):
    with open(RECORD_PATH, "w") as file:
        file.write(f"{new_time},{new_questions},{new_accuracy}")

def verify_key(user_key):
    try:
        response = requests.get(KEYS_URL)
        if response.status_code == 200:
            valid_keys = response.text.splitlines()
            return user_key in valid_keys
        else:
            print(red("❌ 无法连接到服务器，请检查网络。"))
            return False
    except Exception as e:
        print(red(f"⚠️  验证失败: {e}"))
        return False

def easy():
    os.system('cls' if os.name == 'nt' else 'clear')

    # Check if a valid key is already stored
    if os.path.exists(VERIFIED_KEY_PATH):
        with open(VERIFIED_KEY_PATH, "r") as file:
            verified_key = file.read().strip()
        print(green(f"✅ 找到已验证的卡密，自动跳过验证：{verified_key}\n"))
    else:
        print(blue("🔐 请输入您的卡密进行验证: "))
        user_key = input("卡密: ").strip()

        if not verify_key(user_key):
            print(red("❌ 卡密无效！请联系管理员获取正确的卡密。"))
            return

        # Save the verified key to a file for future sessions
        with open(VERIFIED_KEY_PATH, "w") as file:
            file.write(user_key)
        
        print(green("✅ 验证成功！欢迎使用快速练习系统。\n"))

    while True:
        history_time, history_questions, history_accuracy = load_record()

        print('为 haoming 量身定制的一百以内加减运算快速练习')
        reset = input(blue("是否清零记录？输入 'yes' 确认，按回车跳过: "))
        if reset.lower() == 'yes':
            history_time, history_questions, history_accuracy = 0.0, 0, 0.0
            save_record(history_time, history_questions, history_accuracy)
            print(blue("记录已清零！\n"))

        print(blue(f"\n历史记录: 练习总时长 {history_time:.1f} 分钟，练习总题数 {history_questions} 道，总正确率 {history_accuracy:.2f}%\n"))

        input('做好准备，按回车键开始')
        os.system('cls' if os.name == 'nt' else 'clear')

        start_time = time.time()
        time_limit = 60

        correct_count = 0
        wrong_count = 0
        total_attempts = 0

        while True:
            elapsed_time = time.time() - start_time
            remaining_time = time_limit - elapsed_time
            
            if remaining_time <= 0:
                print(blue("\n⏳ 时间到！1 分钟已结束。"))
                break

            print(blue(f"⌛ 剩余时间: {remaining_time:.1f} 秒"))

            number1 = random.randint(0, 100)
            number2 = random.randint(0, 100)
            mark = random.choice('+-')

            user_input = input(f"{number1} {mark} {number2} = ? ").strip()

            if not user_input.lstrip('-').isdigit():
                print(red("⚠️ 请输入有效的数字！"))
                continue

            answer = int(user_input)
            answer_auto = number1 + number2 if mark == '+' else number1 - number2
            total_attempts += 1

            if answer == answer_auto:
                print(green('✅ 正确！🎉'))
                correct_count += 1
            else:
                print(red("❌ 错误！"))
                print(red(f"你的答案: {answer}"))
                print(green(f"正确答案: {answer_auto}"))
                wrong_count += 1

        new_total_time = history_time + (elapsed_time / 60)
        new_total_questions = history_questions + total_attempts
        accuracy = (correct_count / total_attempts) * 100 if total_attempts > 0 else 0
        new_total_accuracy = ((history_accuracy * history_questions) + (accuracy * total_attempts)) / new_total_questions if new_total_questions > 0 else 0

        save_record(new_total_time, new_total_questions, new_total_accuracy)

        print("\n📊 练习总结：")
        print(green(f"✅ 正确次数: {correct_count}"))
        print(red(f"❌ 错误次数: {wrong_count}"))
        print(green(f"🎯 本轮正确率: {accuracy:.2f}%"))
        print(blue(f"📌 本轮做题数量: {total_attempts}"))
        print(blue(f"⏳ 总练习时间: {new_total_time:.1f} 分钟"))
        print(blue(f"🏆 总正确率: {new_total_accuracy:.2f}%"))

        retry = input(blue("\n是否再来一轮？(yes 继续 / 其他键退出): "))
        if retry.lower() != 'yes':
            print(green("👋 训练结束，欢迎下次再来！"))
            break

easy()
