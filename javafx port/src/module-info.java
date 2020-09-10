module hackathone {
    requires javafx.controls;
    requires javafx.fxml;
    requires java.desktop;

    opens controllers;
    opens fxml;
    opens main;
}