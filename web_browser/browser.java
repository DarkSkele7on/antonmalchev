import java.awt.BorderLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.IOException;

import javax.swing.JEditorPane;
import javax.swing.JFrame;
import javax.swing.JScrollPane;
import javax.swing.JTextField;

class SimpleBrowser extends JFrame {
  private JTextField addressBar;
  private JEditorPane display;
  // constructor
  public SimpleBrowser() {
    super("Simple Browser");

    addressBar = new JTextField("Enter a URL!");
    addressBar.addActionListener(
            new ActionListener() {
              public void actionPerformed(ActionEvent event) {
                loadCrap(event.getActionCommand());
              }
            }
    );
    add(addressBar, BorderLayout.NORTH);

    display = new JEditorPane();
    display.setEditable(false);
    //display.addHyperlinkListener(new LinkListener());

    add(new JScrollPane(display), BorderLayout.CENTER);
    setSize(500, 300);
    setVisible(true);
  }

  // load crap to display on the screen
  private void loadCrap(String userText) {
    try {
      display.setPage(userText);
      addressBar.setText(userText);
    } catch (IOException e) {
      System.out.println("Crap cannot be loaded: " + e);
    }
  }
}
