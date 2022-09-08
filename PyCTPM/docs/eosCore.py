# equation of states
# -------------------

# import packages/modules
import numpy as np
import math
# internals
import PyCTPM.core.constants as CONST
from PyCTPM.docs.eos import eosClass
from PyCTPM.docs.eosData import dbClass


class eosCoreClass(eosClass):
    # number of components
    componentsNo = 0
    # init

    def __init__(self, compData, components, eosName, moleFraction, params):
        self.compData = compData
        self.components = components
        self.eosName = eosName
        self.moleFraction = moleFraction
        self.params = params
        # set PVT
        self.P = params.get("pressure", 0)
        self.T = params.get("temperature", 0)
        self.componentsNo = len(self.components)
        # parent
        super().__init__(self.P, self.T, eosName, moleFraction)

    def classDes():
        print("functions used by all equation of states")

    def _eosPR(self):
        '''
        find compressibility factor (Z) at specified P and T
        then molar-volume is found.

        output:
            res:
                pressure: fixed pressure [Pa]
                temperature: fixed temperature [K]
                molar-volumes: for all Z [m^3/mol]
                gas: for the highest Z [m^3/mol]
                liquid: for the lowest Z [m^3/mol]
                Z: compressibility coefficient [-]
                eos-params: a,b,A,B,alpha,beta,gamma
        '''
        try:
            # component data
            componentsData = self.compData

            # sorted data
            # Pc [bar], Tc [K], w [-]
            # ! Pc [bar] => [Pa]
            componentsDataSorted = [
                [float(item['Pc'])*1e5, float(item['Tc']), float(item['w'])] for item in componentsData]

            # set a b matrix
            a = np.zeros(self.componentsNo)
            b = np.zeros(self.componentsNo)

            count = 0
            for item in componentsDataSorted:
                aLoop = self.aPR(item[0], item[1], item[2])
                # a.append(aLoop)
                a[count] = aLoop
                bLoop = self.bPR(item[0], item[1])
                # b.append(bLoop)
                b[count] = bLoop

                # T/Tc ratio
                T_Tc_ratio = self.T/item[1]

                # set
                count += 1

            # check pure, multi-component system
            if self.componentsNo > 1:
                # mixing rule to calculate a/b
                # kij
                kij = self.kijFill()
                aij = self.aijFill(a, kij)
                aSet = self.aMixing(aij, self.moleFraction)
                bSet = self.bMixing(b, self.moleFraction)
            else:
                # no change a/b (pure component)
                aSet = a[0]
                bSet = b[0]

            # set parameters A,B
            A = self.eos_A(aSet)
            B = self.eos_B(bSet)

            # build polynomial eos equation f(Z)
            alpha = self.eos_alpha(B)
            beta = self.eos_beta(A, B)
            gamma = self.eos_gamma(A, B)

            # eso-params
            esoParams = {
                "a": aSet,
                "b": bSet,
                "A": A,
                "B": B,
                "alpha": alpha,
                "beta": beta,
                "gamma": gamma
            }

            # find f(Z) root
            rootList = np.sort(self.findRootfZ(alpha, beta, gamma))

            #! check how many real Z
            ZsNo = len(rootList)

            # z
            minZ = np.amin(rootList)
            maxZ = np.amax(rootList)

            # molar-volume [m3/mol]
            # -> all
            molarVolumes = np.sort(self.molarVolume(rootList))
            # -> liquid
            molarVolumeLiquid = self.molarVolume(minZ)
            # -> gas
            molarVolumeGas = self.molarVolume(maxZ)

            # REVIEW
            # calculate specific volume [m^3/kg]
            # res
            res = {
                "pressure": self.P,
                "temperature": self.T,
                "molar-volumes": molarVolumes,
                "gas": molarVolumeGas,
                "liquid": molarVolumeLiquid,
                "Z": rootList,
                "eos-params": esoParams,
            }

            return molarVolumes, rootList, esoParams, T_Tc_ratio

        except Exception as e:
            raise Exception(e)

    def _eosMixPR(self):
        '''
        find compressibility factor (Z) at specified P and T
        then molar-volume is found.

        output:
            res:
                pressure: fixed pressure [Pa]
                temperature: fixed temperature [K]
                molar-volumes: for all Z [m^3/mol]
                gas: for the highest Z [m^3/mol]
                liquid: for the lowest Z [m^3/mol]
                Z: compressibility coefficient [-]
                eos-params: a,b,A,B,alpha,beta,gamma
        '''
        try:
            # component data
            componentsData = self.compData

            # sorted data
            # Pc [bar], Tc [K], w [-]
            # ! Pc [bar] => [Pa]
            componentsDataSorted = [
                [float(item['Pc'])*1e5, float(item['Tc']), float(item['w'])] for item in componentsData]

            # set a b matrix
            a = np.zeros(self.componentsNo)
            b = np.zeros(self.componentsNo)

            count = 0
            for item in componentsDataSorted:
                aLoop = self.aPR(item[0], item[1], item[2])
                # a.append(aLoop)
                a[count] = aLoop
                bLoop = self.bPR(item[0], item[1])
                # b.append(bLoop)
                b[count] = bLoop
                count += 1

            # check pure, multi-component system
            if self.componentsNo > 1:
                # mixing rule to calculate a/b
                # kij
                kij = self.kijFill()
                aij = self.aijFill(a, kij)
                aSet = self.aMixing(aij, self.moleFraction)
                bSet = self.bMixing(b, self.moleFraction)
            else:
                # no change a/b (pure component)
                aSet = a[0]
                bSet = b[0]

            # set parameters A,B
            A = self.eos_A(aSet)
            B = self.eos_B(bSet)

            # build polynomial eos equation f(Z)
            alpha = self.eos_alpha(B)
            beta = self.eos_beta(A, B)
            gamma = self.eos_gamma(A, B)

            # eso-params
            esoParams = {
                "a": aSet,
                "b": bSet,
                "A": A,
                "B": B,
                "alpha": alpha,
                "beta": beta,
                "gamma": gamma
            }

            # find f(Z) root
            rootList = self.findRootfZ(alpha, beta, gamma)

            # z
            minZ = np.amin(rootList)
            maxZ = np.amax(rootList)

            # molar-volume [m3/mol]
            # -> all
            molarVolumes = self.molarVolume(rootList)
            # -> liquid
            molarVolumeLiquid = self.molarVolume(minZ)
            # -> gas
            molarVolumeGas = self.molarVolume(maxZ)

            # REVIEW
            # calculate specific volume [m^3/kg]
            # res
            res = {
                "pressure": self.P,
                "temperature": self.T,
                "molar-volumes": molarVolumes*np.array(self.moleFraction),
                "gas": molarVolumeGas*np.array(self.moleFraction),
                "liquid": molarVolumeLiquid*np.array(self.moleFraction),
                "Z": rootList,
                "eos-params": esoParams
            }

            return res

        except Exception as e:
            raise Exception(e)
