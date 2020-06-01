import tkinter
import tkinter.filedialog
import tkinter.font


class Text:
    def __init__(self , parent )  :
        self.Text = tkinter.Text(parent)
        self.Text.pack(expand=True, fill='both')
        

class Menu:
    def __init__(self , parent):
        self.parent = parent
        self.currentFile = None
        self.Text = parent.winfo_children()[0]
        self.Menu = tkinter.Menu(parent )
        self.File = tkinter.Menu(self.Menu, tearoff=0)
        self.File.add_command(label="New" , command= self.NewFile)
        self.File.add_command(label="Open" , command= self.OpenFile)
        self.File.add_command(label="Save" , command= self.Save)
        self.File.add_command(label="Save as" , command= self.__WriteFile__)
        self.File.add_command(label="Exit" , command= parent.destroy)
        self.Menu.add_cascade(label="File", menu=self.File) #hierarchical menu
        self.parent.bind("<Key>", self.ChangesPerformed)
        self.anychanges = False
                                                                           
        self.Edit = tkinter.Menu(self.Menu, tearoff=0)
        self.Edit.add_command(label="Cut"  , command= self.cut )
        self.Edit.add_command(label="Copy" , command= self.copy)
        self.Edit.add_command(label="Paste" , command= self.paste)
        
        self.Menu.add_cascade(label="Edit", menu=self.Edit) #hierarchical menu
        self.selectedstring = ""
        
        self.Font = tkinter.Menu(self.Menu, tearoff=0)
        self.Font.add_command(label="Font" ,command= self.FontDialogBox)
        self.Menu.add_cascade(label="Font", menu=self.Font) #hierarchical menu
        
    
    def NewFile(self):
        if not((self.anychanges and self.BlankFile()) or not self.anychanges): 
            self.__WriteFile__()
        self.Text.delete("1.0",tkinter.END)
        self.currentFile = None
        self.anychanges = False
            
    def OpenFile(self):
        if not((self.anychanges and self.BlankFile()) or not self.anychanges): 
            self.__WriteFile__()
        file = tkinter.filedialog.askopenfilename(filetypes=[("Text", ".txt")])
        if file:
            with open(file, 'r') as fp:
                self.Text.delete("1.0",tkinter.END)
                self.Text.insert('1.0' , fp.read())
            self.currentFile = file
            self.anychanges = False
            
    def Save(self):
        if (self.currentFile == None):
            self.__WriteFile__()
        else:
            text = self.Text.get("1.0",tkinter.END) #from line one, character zero
            with open(self.currentFile, 'w') as fp: 
                fp.write(text)
        self.anychanges = False
    
            
    def __WriteFile__(self):
        text = self.Text.get("1.0",tkinter.END) #from line one, character zero
        file = tkinter.filedialog.asksaveasfilename(filetypes=[("Text", ".txt")])
        if file:
            with open(file, 'w') as fp: 
                fp.write(text)
            self.currentFile = file
            self.anychanges = False
            
    def BlankFile(self):
        if (len(self.Text.get("1.0",tkinter.END))==1):
            return True
        else:
            return False
        
    def ChangesPerformed(self , event):
        self.anychanges = True
        
        
        
        
    def cut(self): 
        self.selectedstring = self.Text.get(tkinter.SEL_FIRST, tkinter.SEL_LAST)
        self.Text.delete(tkinter.SEL_FIRST, tkinter.SEL_LAST)
    
    def copy(self):
        self.selectedstring = self.Text.get(tkinter.SEL_FIRST, tkinter.SEL_LAST)
        
    def paste(self):
        self.Text.insert(tkinter.INSERT , self.selectedstring)
    
    def FontDialogBox(self):
        Font(self.Text)
        
class Font:
    def __init__(self , parent):
        self.parent = parent
        self.window = tkinter.Toplevel()
        self.varfont = tkinter.StringVar()
        self.varweight  = tkinter.StringVar()
        self.varslant = tkinter.StringVar()
        self.varsize = tkinter.IntVar()
        self.FontFamily()
        self.Weight()
        self.Slant()  
        self.Size()
        self.Options()
        
        
        
        
    def FontFamily(self):
        family = tkinter.Frame(self.window)
        family.pack(side =  tkinter.LEFT)
        tkinter.Label( family, text="Font" ).pack(anchor = tkinter.W)
        for i,x in enumerate(tkinter.font.families()):
            tkinter.Radiobutton(family, text=x , variable = self.varfont ,  value=x).pack(anchor = tkinter.W)
        
    def Weight(self):
        weight = tkinter.Frame(self.window)
        weight.pack(side =  tkinter.LEFT)
        tkinter.Label( weight, text="Weight" ).pack(anchor = tkinter.W)
        for i,x in enumerate(["normal", "bold"]):
            tkinter.Radiobutton(weight, text=x , variable = self.varweight, value=x).pack(anchor = tkinter.W)
        
    def Slant(self):
        slant = tkinter.Frame(self.window)
        slant.pack(side =  tkinter.LEFT)
        tkinter.Label( slant, text="Slant" ).pack(anchor = tkinter.W)
        for i,x in enumerate(["roman", "italic"]):
            tkinter.Radiobutton(slant, text=x, variable = self.varslant,  value=x).pack(anchor = tkinter.W)
            
    def Size(self):
        size = tkinter.Frame(self.window)
        size.pack(side =  tkinter.LEFT)
        tkinter.Label( size, text="Size" ).pack(anchor = tkinter.W)
        tkinter.Scale( size, variable = self.varsize ).pack(anchor = tkinter.W)
      
    def Options(self):
        frame = tkinter.Frame(self.window)
        frame.pack(side = tkinter.BOTTOM)
        Ok = tkinter.Button(frame , text = "Ok" , command= self.ChangeFont)
        Ok.pack(side = tkinter.LEFT)
        Cancel = tkinter.Button(frame , text = "Cancel" , command = self.window.destroy)
        Cancel.pack(side = tkinter.LEFT)
        
    def ChangeFont(self):
        Font = tkinter.font.Font(family=self.varfont.get(), weight = self.varweight.get() , slant = self.varslant.get() , size= self.varsize.get())
        self.parent.configure(font= Font)
        self.window.destroy()

if __name__ == "__main__":
    notepad = tkinter.Tk()
    Text_Block = Text(notepad)
    Menu_Box = Menu(notepad) 
    notepad.config(menu=Menu_Box.Menu)
    notepad.mainloop()


