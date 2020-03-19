from pydub import AudioSegment

sound = AudioSegment.from_mp3("C:\\Users\\User\\Desktop\\GoogleAPI\\happy.mp3")
sound.export("C:\\Users\\User\\Desktop\\ChangeSound\\happy123123.flac", format="flac")

