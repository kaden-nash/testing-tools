public class Person {
    public String name;
    public double rate;
    public double hours;

    public static void main (String[] args) {
        Person p = new Person("john", 10);
        System.out.println(p.getName() + " " + p.getRate());
    }

    public Person(String name, double rate) {
        this.name = name;
        this.rate = rate;
    }

    // getters
    public String getName() {
        return name;
    }

    public double getRate() {
        return rate;
    }

    // setters
    public void setName(String name) {
        this.name = name;
    }

    public void setRate(double rate) {
        this.rate = rate;
    }

    public void setInformation(String name, double rate) {
        this.name = name;
        this.rate = rate;
    }
}