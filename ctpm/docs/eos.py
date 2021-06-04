# eos class
# parameters for three equation of states
# van der Waals
# Redlich-Kwong and Soave
# Peng-Robinson

class eosClass:
    # init
    def __init__(self, eosName) -> None:
        self.eosName = eosName

     #! alpha
    def eos_alpha(self, B):
        # var
        res = 0
        # eos name
        eosNameSet = self.eosName

        # select eos
        switchDic = {
            "van-der-waals": lambda B: -1 - B,
            "redlich-kwong-soave": lambda B: -1,
            "peng-robinson": lambda B: -1 + B,
        }

        # res
        res = switchDic.get(eosNameSet)(B)

        return res

#   #! beta
#     def eos_beta(eosName, A, B):
#     switch(eosName) {
#       case "van-der-waals":
#         return A;

#       case "redlich-kwong":
#       case "soave":
#         return A - B - Math.pow(B, 2);

#       case "peng-robinson":
#         return A - 3 * Math.pow(B, 2) - 2 * B;}

#   #! gamma
#   def eos_gamma(eosName, A, B):
#     switch (eosName) {
#       case "van-der-waals":
#         return -A * B;

#       case "redlich-kwong":
#       case "soave":
#         return -A * B;

#       case "peng-robinson":
#         return -A * B + Math.pow(B, 2) + Math.pow(B, 3);
#     }
