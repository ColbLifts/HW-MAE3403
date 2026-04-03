import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from pyXSteam.XSteam import XSteam

#Gemini was used in generating this code.

#UNIT CONVERSION

class UC:
    # Basic conversion factors
    bar_to_psi = 14.5038
    m3kg_to_ft3lb = 16.0185
    kJkg_to_btulb = 0.429923
    kJkgC_to_btulbF = 0.238846

    @staticmethod
    def C_to_F(C): return (C * 9 / 5) + 32

    @staticmethod
    def F_to_C(F): return (F - 32) * 5 / 9



# THE THERMOSTATE CLASS

class thermoState:
    def __init__(self):
        self.p = 0;
        self.T = 0;
        self.x = 0;
        self.u = 0;
        self.h = 0;
        self.s = 0;
        self.v = 0
        self.SI = True

    def setState(self, p1_name, p2_name, p1_val, p2_val, SI=True):
        self.SI = SI
        # XSteam
        st = XSteam(XSteam.UNIT_SYSTEM_MKS if SI else XSteam.UNIT_SYSTEM_FLS)

        #(P-T, P-X, T-X).

        try:
            if p1_name == 'p' and p2_name == 't':
                self.p, self.T = p1_val, p2_val
                self.h = st.h_pt(p1_val, p2_val)
                self.s = st.s_pt(p1_val, p2_val)
                self.u = st.u_pt(p1_val, p2_val)
                self.v = st.v_pt(p1_val, p2_val)
                self.x = st.x_pt(p1_val, p2_val)
            elif p1_name == 'p' and p2_name == 'x':
                self.p, self.x = p1_val, p2_val
                self.T = st.tsat_p(p1_val)
                self.h = st.h_px(p1_val, p2_val)

        except:
            pass

    def __sub__(self, other):
        """Calculates State Change (Self - Other)"""
        diff = thermoState()
        diff.p = self.p - other.p
        diff.T = self.T - other.T
        diff.u = self.u - other.u
        diff.h = self.h - other.h
        diff.s = self.s - other.s
        diff.v = self.v - other.v
        return diff



#THE UI & APPLICATION LOGIC

class ThermoApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.SI_Prev = True  # Keep track of unit state
        self.setupUi()
        self.show()

    def setupUi(self):
        self.setObjectName("StateCalc")
        self.resize(1000, 600)
        self.main_layout = QtWidgets.QVBoxLayout(self)

        # UNITS PART
        self._grp_Units = QtWidgets.QGroupBox("System of Units")
        unit_layout = QtWidgets.QHBoxLayout(self._grp_Units)
        self._rdo_SI = QtWidgets.QRadioButton("SI");
        self._rdo_SI.setChecked(True)
        self._rdo_English = QtWidgets.QRadioButton("English")
        unit_layout.addWidget(self._rdo_SI);
        unit_layout.addWidget(self._rdo_English)
        self.main_layout.addWidget(self._grp_Units)

        # INPUT SECTION (STATE 1 & STATE 2)
        self._grp_Inputs = QtWidgets.QGroupBox("Specified Properties")
        grid = QtWidgets.QGridLayout(self._grp_Inputs)
        props = ["Pressure (p)", "Temperature (T)", "Quality (x)", "Enthalpy (h)"]

        # STATE 1
        grid.addWidget(QtWidgets.QLabel("<b>State 1</b>"), 0, 0)
        self._cmb_Property1 = QtWidgets.QComboBox();
        self._cmb_Property1.addItems(props)
        self._le_Property1 = QtWidgets.QLineEdit("1.0")
        self._lbl_U1 = QtWidgets.QLabel("bar")
        self._cmb_Property2 = QtWidgets.QComboBox();
        self._cmb_Property2.addItems(props);
        self._cmb_Property2.setCurrentIndex(1)
        self._le_Property2 = QtWidgets.QLineEdit("100.0")
        self._lbl_U2 = QtWidgets.QLabel("C")
        grid.addWidget(self._cmb_Property1, 1, 0);
        grid.addWidget(self._le_Property1, 1, 1);
        grid.addWidget(self._lbl_U1, 1, 2)
        grid.addWidget(self._cmb_Property2, 2, 0);
        grid.addWidget(self._le_Property2, 2, 1);
        grid.addWidget(self._lbl_U2, 2, 2)

        # STATE 2
        grid.addWidget(QtWidgets.QLabel("<b>State 2</b>"), 0, 3)
        self._cmb_Property1_State2 = QtWidgets.QComboBox();
        self._cmb_Property1_State2.addItems(props)
        self._le_Property1_State2 = QtWidgets.QLineEdit("2.0")
        self._lbl_U1_S2 = QtWidgets.QLabel("bar")
        self._cmb_Property2_State2 = QtWidgets.QComboBox();
        self._cmb_Property2_State2.addItems(props);
        self._cmb_Property2_State2.setCurrentIndex(1)
        self._le_Property2_State2 = QtWidgets.QLineEdit("200.0")
        self._lbl_U2_S2 = QtWidgets.QLabel("C")
        grid.addWidget(self._cmb_Property1_State2, 1, 3);
        grid.addWidget(self._le_Property1_State2, 1, 4);
        grid.addWidget(self._lbl_U1_S2, 1, 5)
        grid.addWidget(self._cmb_Property2_State2, 2, 3);
        grid.addWidget(self._le_Property2_State2, 2, 4);
        grid.addWidget(self._lbl_U2_S2, 2, 5)

        self.main_layout.addWidget(self._grp_Inputs)

        # CALCULATE BUTTON
        self._pb_Calculate = QtWidgets.QPushButton("Calculate")
        self._pb_Calculate.clicked.connect(self.calculateProperties)
        self.main_layout.addWidget(self._pb_Calculate)

        #  RESULTS SECTION
        self._grp_Results = QtWidgets.QGroupBox("State Properties")
        res_layout = QtWidgets.QHBoxLayout(self._grp_Results)
        self._lbl_S1_Res = QtWidgets.QLabel("State 1\n---");
        self._lbl_S1_Res.setFrameStyle(QtWidgets.QFrame.Panel)
        self._lbl_S2_Res = QtWidgets.QLabel("State 2\n---");
        self._lbl_S2_Res.setFrameStyle(QtWidgets.QFrame.Panel)
        self._lbl_Del_Res = QtWidgets.QLabel("State Change (Δ)\n---");
        self._lbl_Del_Res.setFrameStyle(QtWidgets.QFrame.Panel)
        res_layout.addWidget(self._lbl_S1_Res);
        res_layout.addWidget(self._lbl_S2_Res);
        res_layout.addWidget(self._lbl_Del_Res)
        self.main_layout.addWidget(self._grp_Results)


        self._rdo_SI.clicked.connect(self.setUnits)
        self._rdo_English.clicked.connect(self.setUnits)

    def setUnits(self):
        """Converts numerical values when the SI/English radio button is clicked."""
        is_SI = self._rdo_SI.isChecked()
        if is_SI == self.SI_Prev: return

        #Conversion for Temperature inputs
        for le in [self._le_Property1, self._le_Property2, self._le_Property1_State2, self._le_Property2_State2]:
            val = float(le.text())
            if is_SI:  # F to C
                le.setText(f"{UC.F_to_C(val):.3f}")
            else:  # C to F
                le.setText(f"{UC.C_to_F(val):.3f}")

        # labels (bar vs psi, C vs F)
        u_p = "bar" if is_SI else "psi"
        u_t = "C" if is_SI else "F"
        self._lbl_U1.setText(u_p);
        self._lbl_U1_S2.setText(u_p)
        self._lbl_U2.setText(u_t);
        self._lbl_U2_S2.setText(u_t)

        self.SI_Prev = is_SI

    def calculateProperties(self):
        SI = self._rdo_SI.isChecked()
        s1 = thermoState();
        s2 = thermoState()

        # State 1 Math
        p1n = self._cmb_Property1.currentText()[-2:-1].lower()
        p2n = self._cmb_Property2.currentText()[-2:-1].lower()
        s1.setState(p1n, p2n, float(self._le_Property1.text()), float(self._le_Property2.text()), SI)

        # State 2 Math
        p1n2 = self._cmb_Property1_State2.currentText()[-2:-1].lower()
        p2n2 = self._cmb_Property2_State2.currentText()[-2:-1].lower()
        s2.setState(p1n2, p2n2, float(self._le_Property1_State2.text()), float(self._le_Property2_State2.text()), SI)

        # Delta Math
        delta = s2 - s1

        # Format output
        p_u = "bar" if SI else "psi";
        t_u = "C" if SI else "F"

        def make_text(st, title):
            return f"<b>{title}</b><br>P: {st.p:.2f} {p_u}<br>T: {st.T:.2f} {t_u}<br>h: {st.h:.2f} kJ/kg"

        self._lbl_S1_Res.setText(make_text(s1, "State 1"))
        self._lbl_S2_Res.setText(make_text(s2, "State 2"))
        self._lbl_Del_Res.setText(make_text(delta, "State Change (Δ)"))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = ThermoApp()
    sys.exit(app.exec_())