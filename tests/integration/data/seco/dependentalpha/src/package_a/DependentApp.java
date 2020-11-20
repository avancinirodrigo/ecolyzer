import package_a.CentralSoftware;

class DependentApp {
	private CentralSoftware central;
	
	public static void main(String[] args) {
		central = DependentCentralFactory.createCentralSoftware();
		int var = central.getVar();
		CentralSoftware other = new CentralSoftware();
		int ovar = other.getVarCopy() + getVarByCentral(central) + var;
		int vvar = getVarByCentral(new CentralSoftware());
	}

	private int getVarByCentral(CentralSoftware central) {
		return central.getVarRef();
	}
}