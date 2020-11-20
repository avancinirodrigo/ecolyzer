import package_a.CentralSoftware;

public class DependentCentralFactory {

	public static CentralSoftware createCentralSoftware() {
		return new CentralSoftware();
	}
}