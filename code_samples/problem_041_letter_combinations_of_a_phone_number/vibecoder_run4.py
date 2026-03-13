class Solution:
    def letterCombinations(self, digits: str) -> List[str]:
        if not digits: return []
        m = {'2':'abc','3':'def','4':'ghi','5':'jkl','6':'mno','7':'pqrs','8':'tuv','9':'wxyz'}
        r = ['']
        for d in digits:
            r = [x + c for x in r for c in m[d]]
        return r