from mail_crew.tools.gmail_utility import authenticate_gmail

def main():
    print("开始 Gmail 认证流程...")
    try:
        service = authenticate_gmail()
        print("认证成功！token.json 文件已生成。")
    except Exception as e:
        print(f"认证过程中出现错误: {e}")

if __name__ == "__main__":
    main() 