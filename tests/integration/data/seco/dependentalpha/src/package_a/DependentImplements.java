import package_a.CentralInterface;

public class DependentSoftware implements CentralInterface {
	private int var;

	void centralInterfaceMethod() {
		CentralSoftware central = createCentralSoftware();
		var = central.getVar();
	}

	CentralSoftware createCentralSoftware() {
		return CentralFactory.createCentralSoftware();
	}
}