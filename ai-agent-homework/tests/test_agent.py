import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from agent import SmartAssistant


def test_add_task():
    print("Test 1: Add Task")
    assistant = SmartAssistant()
    response = assistant.process("add task: Finish homework")
    assert response["success"] == True
    print("  OK -", response["message"][:50])


def test_list_tasks():
    print("\nTest 2: List Tasks")
    assistant = SmartAssistant()
    assistant.process("add task: Buy milk")
    response = assistant.process("list tasks")
    assert response["success"] == True
    print("  OK")


def test_complete_task():
    print("\nTest 3: Complete Task")
    assistant = SmartAssistant()
    assistant.process("add task: Test task")
    response = assistant.process("complete task 1")
    assert response["success"] == True
    print("  OK -", response["message"])


def test_weather():
    print("\nTest 4: Weather Query")
    assistant = SmartAssistant()
    response = assistant.process("weather in Beijing")
    assert response["success"] == True
    print("  OK -", response["message"].split("\n")[0][:50])


def test_help():
    print("\nTest 5: Help Command")
    assistant = SmartAssistant()
    response = assistant.process("help")
    assert response["success"] == True
    print("  OK")


def test_conversation_memory():
    print("\nTest 6: Conversation Memory")
    assistant = SmartAssistant()
    assistant.process("add task: Test memory")
    history = assistant.get_history()
    assert len(history) >= 2
    print("  OK - History length:", len(history))


def test_multiple_tasks():
    print("\nTest 7: Multiple Tasks")
    assistant = SmartAssistant()
    assistant.process("add task: Task 1")
    assistant.process("add task: Task 2")
    assistant.process("add task: Task 3")
    response = assistant.process("list tasks")
    assert response["success"] == True
    print("  OK")


def test_delete_task():
    print("\nTest 8: Delete Task")
    assistant = SmartAssistant()
    assistant.process("add task: Task to delete")
    response = assistant.process("delete task 1")
    assert response["success"] == True
    print("  OK -", response["message"])


def test_clear_history():
    print("\nTest 9: Clear History")
    assistant = SmartAssistant()
    assistant.process("Hello")
    response = assistant.process("clear history")
    assert response["success"] == True
    print("  OK -", response["message"])


def test_chat():
    print("\nTest 10: Chat")
    assistant = SmartAssistant()
    response = assistant.process("Hello there")
    assert response["success"] == True
    assert len(response["message"]) > 0
    print("  OK")


def run_all_tests():
    print("=" * 50)
    print("Running AI Agent Tests")
    print("=" * 50)

    tests = [
        test_add_task,
        test_list_tasks,
        test_complete_task,
        test_weather,
        test_help,
        test_conversation_memory,
        test_multiple_tasks,
        test_delete_task,
        test_clear_history,
        test_chat,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print("\n  FAIL:", str(e))
            failed += 1

    print("\n" + "=" * 50)
    print("Results:", passed, "passed,", failed, "failed")
    print("=" * 50)

    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
