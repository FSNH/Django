import re


class IsCas(object):
    """
    CAS编号以升序排列且代表其重要程度和命名早晚。一个CAS编号以连字符“-”分为三部分，第一部分有2到6位数字，第二部分有2位数字，第三部分有1位数字作为校验码。校验码的计算方法如下：CAS
    顺序号（第一、二部分数字）的最后一位乘以1，最后第二位乘以2，依此类推，然后再把所有的乘积相加，再把和除以10，其余数就是第三部分的校验码。 举例来说，水 的CAS编号前两部分是7732-18，则其校验码= ( 8×1 +
    1×2 + 2×3 + 3×4 + 7×5 + 7×6 ) dim 10 = 105 mod 10 = 5（mod为求余运算符），所以水的CAS为7732-18-5。
    """

    @classmethod
    def iscas(cls, cas: str):
        if cas:
            patter = re.compile(r"^[0-9]{2,7}-[0-9]{2}-[0-9]$")
            result = patter.findall(cas)  # 正则匹配cas
            # print(result)['7732-18-5']
            global flag
            flag = False
            if result:  # 列表不为空
                teststring = cas[:cas.rindex('-')]  # 获取cas号第一个到最后一个'-'之前的字符
                teststring = teststring.replace('-', '')  # 空格替换'-'
                # print("teststring:" + teststring)
                lastchar = cas[-1]  # 获取最后一个字符
                # print(lastchar)
                total = 0
                # print(f"len：{','.join(teststring).split(',')}")
                for i in range(1, len(','.join(teststring).split(',')) + 1):
                    total += int(teststring[-i]) * i
                    # print(total)
                mod = total % 10  # 总和与10取余
                # print(mod)
                if lastchar == str(mod):
                    flag = True
                return flag


if __name__ == '__main__':
    a = IsCas.iscas('7732-18-1')
    print(a)
