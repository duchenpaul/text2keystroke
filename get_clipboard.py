import win32clipboard

def get_clipboard():
    win32clipboard.OpenClipboard()
    try:
        data = win32clipboard.GetClipboardData()
    except TypeError as e:
        print('No text in the clipboard.')
    else:   
        win32clipboard.CloseClipboard()
        return data


if __name__ == '__main__':
    print(get_clipboard())