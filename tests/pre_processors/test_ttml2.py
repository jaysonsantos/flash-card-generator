from learning.pre_processors.subtitles.ttml2 import TTML2PreProcessor

EXAMPLE = """<?xml version="1.0" encoding="utf-8"?>
<tt xmlns="http://www.w3.org/ns/ttml" xmlns:tts="http://www.w3.org/ns/ttml#styling"
    ttp:version="2" xmlns:ttm="http://www.w3.org/ns/ttml#metadata"
    xmlns:ttp="http://www.w3.org/ns/ttml#parameter" xml:lang="de">
 <body>
  <div>
   <p><span>[Sprecher]</span><br />Was bisher geschah...</p>
   <p><span>Wenn Sie heiraten würden,</span><br />zahlen Sie ein Drittel weniger.</p>
   <p><span>Ein Drittel?</span></p>
   <p><span>-Anne, willst du mich heiraten?</span><br />-Was?</p>
   <p><span>Bis morgen kannste es dir noch überlegen.</span></p>
   <p><span>Man muss es einfach durchziehen.</span></p>
   <p><span>Wagen Sie es ja nicht,</span><br />Ihre Freundin zu enttäuschen.</p>
   <p><span>Ich werd mir Mühe geben.</span></p>
   <p><span>Hab mich schon gefragt,</span><br />wann du kalte Füße kriegst.</p>
   <p><span>Wenn ich kalte Füße hätte, wären wir</span><br />gar nicht hier eingezogen.</p>
   <p><span>Und ist doch schön hier, wir haben</span><br />doch 'ne tolle Beziehung!</p>
   <p><span>Ja? Ist das so?</span><br />Ich hab das Gefühl,</p>
   <p><span>wenn wir nicht vor der Glotze hängen,</span><br />haben wir uns nicht viel zu sagen.</p>
  </div>
 </body></tt>
 """.encode()


def test_output():
    pre_processor = TTML2PreProcessor(EXAMPLE)
    expected = """[Sprecher] Was bisher geschah...
Wenn Sie heiraten würden, zahlen Sie ein Drittel weniger.
Ein Drittel?
-Anne, willst du mich heiraten? -Was?
Bis morgen kannste es dir noch überlegen.
Man muss es einfach durchziehen.
Wagen Sie es ja nicht, Ihre Freundin zu enttäuschen.
Ich werd mir Mühe geben.
Hab mich schon gefragt, wann du kalte Füße kriegst.
Wenn ich kalte Füße hätte, wären wir gar nicht hier eingezogen.
Und ist doch schön hier, wir haben doch 'ne tolle Beziehung!
Ja? Ist das so? Ich hab das Gefühl,
wenn wir nicht vor der Glotze hängen, haben wir uns nicht viel zu sagen."""

    for (expected, got) in zip(expected.split("\n"), pre_processor.get_output_text().split("\n")):
        assert expected.strip() == got.strip()
