import package_a.CentralSoftware;

public class DependentSoftware extends CentralSoftware {
	private int var;

	public DependentSoftware() {
		super();
		var = super.getVar();
	}

	public int getVar() {
		return var;
	}
}