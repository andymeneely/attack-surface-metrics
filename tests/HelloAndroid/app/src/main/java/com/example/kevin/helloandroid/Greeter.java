package com.example.kevin.helloandroid;

/**
 * Created by kevin on 2/16/15.
 */
public class Greeter {

    private String name;

    public Greeter(String Name)
    {
        this.name = Name;
    }

    public String getName()
    {
        return this.name;
    }

    public void setName(String value)
    {
        this.name = value;
    }

    public String sayHello()
    {
        return "Hello, " + this.name;
    }

    public String sayHelloInSpanish()
    {
        return "Hola, " + this.name;
    }
}