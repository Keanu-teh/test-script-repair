import codeAdd
import codeRepair

'''
                                    根据GPT输出的结果决定下一步的操作
'''


# 将response传到codeRepair.py和codeAdd.py中并加到注释里
def get_result(result_str):
    if 'possibly' in result_str:
        # 调用代码修复函数进行代码修复并在代码后加上possibly注释
        final_result = codeRepair.choose_repair_function(result_str)
    if 'id =' in result_str and 'possibly' not in result_str and 'click' not in result_str:
        # 调用代码修复函数进行代码修复
        final_result = codeRepair.choose_repair_function(result_str)
    if 'swipe' in result_str:
        # 调用代码添加函数进行代码添加并将bounds属性的值传进去
        final_result = codeAdd.choose_add_function(result_str)
    if 'click id =' in result_str:
        # 调用代码添加函数进行代码添加
        final_result = codeAdd.choose_add_function(result_str)
    if 'only' in result_str:
        final_result = codeRepair.choose_repair_function(result_str)
    if 'function deleted' in result_str:
        # 输出修复失败
        final_result = 'function deleted'

    return final_result


