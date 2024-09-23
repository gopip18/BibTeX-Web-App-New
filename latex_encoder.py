def latex_encode(text):
    latex_chars = {
        'ć': "\\'{c}", '€': '\\euro{}', '‘': "`", '’': "'", '“': '``', '”': "''",
        '‚': ',', 'ƒ': '{\\textflorin}', '„': ',,', '…': '\\ldots', '†': '\\dag',
        '‡': '\\ddag', '‰': '\\textperthousand', 'Š': '\\v{S}', '‹': '\\guilsinglleft',
        'Œ': '\\OE', 'Ž': '\\v{Z}', '•': '\\textbullet', '–': '--', '—': '---',
        '˜': '\\textasciitilde', '™': '\\texttrademark', 'š': '\\v{s}', '›': '\\guilsinglright',
        'œ': '\\oe', 'ž': '\\v{z}', 'Ÿ': '\\textyen',
        '¡': '\\textexclamdown', '¢': '\\textcent', '£': '\\pounds', '¤': '\\textcurrency',
        '¥': '\\yen', '¦': '\\textbrokenbar', '§': '\\S', '¨': '\\textasciidieresis',
        '©': '\\copyright', 'ª': '\\textordfeminine', '«': '\\guillemotleft', '¬': '\\neg',
        '®': '\\textregistered', '¯': '\\textasciimacron', '°': '\\textdegree',
        '±': '\\pm', '²': '^{2}', '³': '^{3}', '´': '\\textasciiacute', 'µ': '\\textmu',
        '¶': '\\P', '·': '\\cdot', '¸': '\\c', '¹': '^{1}', 'º': '\\textordmasculine',
        '»': '\\guillemotright', '¼': '\\textonequarter', '½': '\\textonehalf',
        '¾': '\\textthreequarters', '¿': '\\textquestiondown', 'À': '\\`{A}', 'Á': "\\'{A}",
        'Â': '\\^{A}', 'Ã': '\\~{A}', 'Ä': '\\"{A}', 'Å': '\\AA', 'Æ': '\\AE', 'Ç': '\\c{C}',
        'È': '\\`{E}', 'É': "\\'{E}", 'Ê': '\\^{E}', 'Ë': '\\"{E}', 'Ì': '\\`{I}', 'Í': "\\'{I}",
        'Î': '\\^{I}', 'Ï': '\\"{I}', 'Ð': '\\DH', 'Ñ': '\\~{N}', 'Ò': '\\`{O}', 'Ó': "\\'{O}",
        'Ô': '\\^{O}', 'Õ': '\\~{O}', 'Ö': '\\"{O}', '×': '\\times', 'Ø': '\\O', 'Ù': '\\`{U}',
        'Ú': "\\'{U}", 'Û': '\\^{U}', 'Ü': '\\"{U}', 'Ý': "\\'{Y}", 'Þ': '\\TH', 'ß': '\\ss',
        'à': '\\`{a}', 'á': "\\'{a}", 'â': '\\^{a}', 'ã': '\\~{a}', 'ä': '\\"{a}', 'å': '\\aa',
        'æ': '\\ae', 'ç': '\\c{c}', 'è': '\\`{e}', 'é': "\\'{e}", 'ê': '\\^{e}', 'ë': '\\"{e}',
        'ì': '\\`{i}', 'í': "\\'{i}", 'î': '\\^{i}', 'ï': '\\"{i}', 'ð': '\\dh', 'ñ': '\\~{n}',
        'ò': '\\`{o}', 'ó': "\\'{o}", 'ô': '\\^{o}', 'õ': '\\~{o}', 'ö': '\\"{o}', '÷': '\\div',
        'ø': '\\o', 'ù': '\\`{u}', 'ú': "\\'{u}", 'û': '\\^{u}', 'ü': '\\"{u}', 'ý': "\\'{y}",
        'þ': '\\th', 'ÿ': '\\"{y}', 'č': '\\v{c}'
        # Continue adding mappings as necessary
    }
    for char, latex_char in latex_chars.items():
        text = text.replace(char, latex_char)
    return text