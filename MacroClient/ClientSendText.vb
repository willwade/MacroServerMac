Imports System
Imports System.Net 
Imports System.Net.Sockets

Module Sample
    Sub main(Byval args() As String)
        Dim pbstr As String = My.Computer.Clipboard.GetText()
        ' This needs escaping double quotes. Everything else should be ok. 
        Dim dataStr As String = "{e7ca10ca-4f8d-47ed-8902178849c7a1d5}<subject=""execute_and_get_modifiers""\><command=""send_key""\><normalkey="""
        dataStr = dataStr & pbstr
        dataStr = dataStr & """\><modifier=""0""\><X_MEUser""@user1-4874-305132@""\><X_MELng""9""\><X_STAVersion""1.1.1.1261""\>"
        
        ' Send dataStr to IP or hostname at port 2800
        ' Dont expect to get anything back!
        ' Do provide an alert warning if IP:Port not responding (e.g. Is machine on at x.x.x.x?)
        
        Console.Write(dataStr)
        Console.Read()
    End Sub

    Sub Total(Byval first As Integer, Byval second As Integer)
        Console.Writeline("The total is: {0}", first+second)
    End Sub
End Module

