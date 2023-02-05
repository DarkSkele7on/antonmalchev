using System;
using System.Windows.Forms;

namespace TextReplacementApp
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void Button1_Click(object sender, EventArgs e)
        {
            // Get the text from the text box
            string text = textBox1.Text;

            // Get the selected language from the drop-down menu
            string selectedLanguage = comboBox1.SelectedItem.ToString();

            // Replace all sentences with the same text in a different language
            if (selectedLanguage == "English")
            {
                text = text.Replace(".", "Translated Sentence in English.");
                text = text.Replace("!", "Translated Sentence in English!");
                text = text.Replace("?", "Translated Sentence in English?");
            }
            else if (selectedLanguage == "French")
            {
                text = text.Replace(".", "Phrase traduite en français.");
                text = text.Replace("!", "Phrase traduite en français!");
                text = text.Replace("?", "Phrase traduite en français?");
            }
            else if (selectedLanguage == "German")
            {
                text = text.Replace(".", "Übersetzter Satz auf Deutsch.");
                text = text.Replace("!", "Übersetzter Satz auf Deutsch!");
                text = text.Replace("?", "Übersetzter Satz auf Deutsch?");
            }

            // Update the text in the text box
            textBox1.Text = text;
        }
    }
}
