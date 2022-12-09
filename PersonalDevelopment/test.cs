using System;


DateTime _DateTime = new DateTime();
DateTime _Date = _DateTime.Date();
Console.WriteLine(_Date);

class Suggestion
{
    private string NameOfSuggestion;
    private double Size;
    private string SuggestionType;
    private string Source;
    Suggestion(string NameOfSuggestion, double Size, string SuggestionType, string Source)
    {
        this.NameOfSuggestion = NameOfSuggestion;
        this.Size = Size;
        this.SuggestionType = SuggestionType;
        this.Source = Source;
    }
}
