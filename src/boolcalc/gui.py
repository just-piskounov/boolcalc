from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, Input, Static, DataTable
from textual.containers import Vertical, Horizontal, ScrollableContainer
from itertools import product
from .core import BooleanExpression

class BoolCalc(App):
    CSS = """
    Screen {
        layout: vertical;
        background: #1a1b26;
        color: #c0caf5;
    }
    
    #main-container {
        width: 100%;
        height: 100%;
        padding: 1;
    }
    
    #input {
        width: 80%;
        margin: 2 5;
        border: round #7aa2f7;
        background: #1a1b26;
        color: #c0caf5
    }
    
    #buttons {
        height: auto;
        margin: 1 5;
        padding: 1;
    }
    
    Button {
        width: 16;
        margin-right: 2;
        background: #7aa2f7;
        color: #1a1b26;
    }
    
    #output {
        margin: 1 5;
        padding: 1;
        border: round #7aa2f7;
        min-height: 3;
    }
    
    #table-container {
        height: 50vh;
        margin: 1 5;
        border: round #7aa2f7;
    }
    
    DataTable {
        width: 100%;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical(id="main-container"):
            yield Input(placeholder="Enter expression (e.g. x*y + ~x*z)", id="input")
            with Horizontal(id="buttons"):
                yield Button("Simplify", id="simplify")
                yield Button("Truth Table", id="table")
                yield Button("Clear", id="clear")
            yield Static("", id="output")
            with ScrollableContainer(id="table-container"):
                yield DataTable(zebra_stripes=True, id="table")
        yield Footer()

    def on_mount(self):
        self.query_one("#table", DataTable).display = False

    def on_button_pressed(self, event: Button.Pressed):
        input = self.query_one("#input", Input)
        output = self.query_one("#output", Static)
        table = self.query_one("#table", DataTable)
        
        if event.button.id == "clear":
            input.value = ""
            output.update("")
            table.clear()
            table.display = False
            return
            
        expr = input.value.strip()
        if not expr:
            output.update("[red]Please enter an expression![/]")
            return
            
        try:
            bexpr = BooleanExpression(expr)
            
            if event.button.id == "simplify":
                simplified = bexpr.simplify()
                output.update(f"[bold green]Simplified:[/]\n{simplified}")
                table.display = False
                
            elif event.button.id == "table":
                output.update(f"[bold]Original:[/] {expr}")
                self.generate_truth_table(bexpr)
                table.display = True
                
        except Exception as e:
            output.update(f"[red]Error: {str(e)}[/]")
            table.display = False

    def generate_truth_table(self, expr: BooleanExpression):
        table = self.query_one("#table", DataTable)
        table.clear(columns=True)
        
        variables = sorted(expr.get_variables())
        if not variables:
            return
            
        table.add_columns("Case", *variables, "Result")
        
        for case, values in enumerate(product([False, True], repeat=len(variables))):
            inputs = dict(zip(variables, values))
            result = expr.evaluate(inputs)
            row = [str(case)] + [str(int(v)) for v in values] + [str(int(result))]
            table.add_row(*row)

def main():
    app = BoolCalc()
    app.run()

if __name__ == "__main__":
    main()

