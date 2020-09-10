package controllers;

import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.control.Button;
import javafx.scene.control.RadioButton;
import javafx.scene.control.TextField;
import javafx.scene.control.ToggleGroup;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;

import javax.swing.*;
import javax.swing.filechooser.FileFilter;
import javax.swing.filechooser.FileNameExtensionFilter;
import javax.swing.filechooser.FileSystemView;
import java.io.File;
import java.net.URL;
import java.util.ResourceBundle;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;

public class ViewerController implements Initializable {
    @FXML
    private ImageView viewerIV;
    @FXML
    private Button playButton;
    @FXML
    private RadioButton cameraRB;
    @FXML
    private Button browseButton;
    @FXML
    private TextField inputVideoTF;

    private boolean playing;

    private ScheduledExecutorService timer;

    private File inFile;

    @FXML
    private void onPlayPress(){
        playButton.setText(playing ? "Play" : "Pause");
        playing = !playing;
    }

    @FXML
    private void onRBChange(){
        boolean selected = cameraRB.isSelected();
        browseButton.setDisable(selected);
        inputVideoTF.setDisable(selected);
    }

    @FXML
    private void onInputVideoTFChange(){
        inFile = (inputVideoTF.getText().isEmpty()) ? null : new File(inputVideoTF.getText());
    }

    @FXML
    private void onBrowse(){
        JFileChooser jfc = new JFileChooser(FileSystemView.getFileSystemView().getHomeDirectory());
        jfc.setAcceptAllFileFilterUsed(false);
        jfc.setFileFilter(new FileFilter() {
            @Override
            public boolean accept(File f) {
                return true; // there are many supported formats
            }

            @Override
            public String getDescription() {
                return "Media Files";
            }
        });
        if (jfc.showOpenDialog(null) == JFileChooser.APPROVE_OPTION){
            inFile = jfc.getSelectedFile();
            inputVideoTF.setText(inFile.getPath());
        }
    }

    @Override
    public void initialize(URL url, ResourceBundle resourceBundle) {
        this.timer = Executors.newSingleThreadScheduledExecutor();
        playing = false;

        Runnable getFrame = () -> {
            if (playing) {
                System.out.println("whoo!"); // temp test function; in future this will update the image view
            }
        };

        this.timer.scheduleAtFixedRate(getFrame, 0, 33, TimeUnit.MILLISECONDS);
    }
}
