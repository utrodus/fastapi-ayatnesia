from dataclasses import dataclass
from typing import Any, List, TypeVar, Type, cast, Callable


T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


@dataclass
class Audio:
    alafasy: str
    ahmedajamy: str
    husarymujawwad: str
    minshawi: str
    muhammadayyoub: str
    muhammadjibreel: str

    @staticmethod
    def from_dict(obj: Any) -> 'Audio':
        assert isinstance(obj, dict)
        alafasy = from_str(obj.get("alafasy"))
        ahmedajamy = from_str(obj.get("ahmedajamy"))
        husarymujawwad = from_str(obj.get("husarymujawwad"))
        minshawi = from_str(obj.get("minshawi"))
        muhammadayyoub = from_str(obj.get("muhammadayyoub"))
        muhammadjibreel = from_str(obj.get("muhammadjibreel"))
        return Audio(alafasy, ahmedajamy, husarymujawwad, minshawi, muhammadayyoub, muhammadjibreel)

    def to_dict(self) -> dict:
        result: dict = {}
        result["alafasy"] = from_str(self.alafasy)
        result["ahmedajamy"] = from_str(self.ahmedajamy)
        result["husarymujawwad"] = from_str(self.husarymujawwad)
        result["minshawi"] = from_str(self.minshawi)
        result["muhammadayyoub"] = from_str(self.muhammadayyoub)
        result["muhammadjibreel"] = from_str(self.muhammadjibreel)
        return result


@dataclass
class Image:
    primary: str
    secondary: str

    @staticmethod
    def from_dict(obj: Any) -> 'Image':
        assert isinstance(obj, dict)
        primary = from_str(obj.get("primary"))
        secondary = from_str(obj.get("secondary"))
        return Image(primary, secondary)

    def to_dict(self) -> dict:
        result: dict = {}
        result["primary"] = from_str(self.primary)
        result["secondary"] = from_str(self.secondary)
        return result


@dataclass
class Sajda:
    recommended: bool
    obligatory: bool

    @staticmethod
    def from_dict(obj: Any) -> 'Sajda':
        assert isinstance(obj, dict)
        recommended = from_bool(obj.get("recommended"))
        obligatory = from_bool(obj.get("obligatory"))
        return Sajda(recommended, obligatory)

    def to_dict(self) -> dict:
        result: dict = {}
        result["recommended"] = from_bool(self.recommended)
        result["obligatory"] = from_bool(self.obligatory)
        return result


@dataclass
class Meta:
    juz: int
    page: int
    manzil: int
    ruku: int
    hizb_quarter: int
    sajda: Sajda

    @staticmethod
    def from_dict(obj: Any) -> 'Meta':
        assert isinstance(obj, dict)
        juz = from_int(obj.get("juz"))
        page = from_int(obj.get("page"))
        manzil = from_int(obj.get("manzil"))
        ruku = from_int(obj.get("ruku"))
        hizb_quarter = from_int(obj.get("hizbQuarter"))
        sajda = Sajda.from_dict(obj.get("sajda"))
        return Meta(juz, page, manzil, ruku, hizb_quarter, sajda)

    def to_dict(self) -> dict:
        result: dict = {}
        result["juz"] = from_int(self.juz)
        result["page"] = from_int(self.page)
        result["manzil"] = from_int(self.manzil)
        result["ruku"] = from_int(self.ruku)
        result["hizbQuarter"] = from_int(self.hizb_quarter)
        result["sajda"] = to_class(Sajda, self.sajda)
        return result


@dataclass
class Number:
    in_quran: int
    in_surah: int

    @staticmethod
    def from_dict(obj: Any) -> 'Number':
        assert isinstance(obj, dict)
        in_quran = from_int(obj.get("inQuran"))
        in_surah = from_int(obj.get("inSurah"))
        return Number(in_quran, in_surah)

    def to_dict(self) -> dict:
        result: dict = {}
        result["inQuran"] = from_int(self.in_quran)
        result["inSurah"] = from_int(self.in_surah)
        return result


@dataclass
class Kemenag:
    short: str
    long: str

    @staticmethod
    def from_dict(obj: Any) -> 'Kemenag':
        assert isinstance(obj, dict)
        short = from_str(obj.get("short"))
        long = from_str(obj.get("long"))
        return Kemenag(short, long)

    def to_dict(self) -> dict:
        result: dict = {}
        result["short"] = from_str(self.short)
        result["long"] = from_str(self.long)
        return result


@dataclass
class Tafsir:
    kemenag: Kemenag
    quraish: str
    jalalayn: str

    @staticmethod
    def from_dict(obj: Any) -> 'Tafsir':
        assert isinstance(obj, dict)
        kemenag = Kemenag.from_dict(obj.get("kemenag"))
        quraish = from_str(obj.get("quraish"))
        jalalayn = from_str(obj.get("jalalayn"))
        return Tafsir(kemenag, quraish, jalalayn)

    def to_dict(self) -> dict:
        result: dict = {}
        result["kemenag"] = to_class(Kemenag, self.kemenag)
        result["quraish"] = from_str(self.quraish)
        result["jalalayn"] = from_str(self.jalalayn)
        return result


@dataclass
class Ayah:
    number: Number
    arab: str
    translation: str
    audio: Audio
    image: Image
    tafsir: Tafsir
    meta: Meta

    @staticmethod
    def from_dict(obj: Any) -> 'Ayah':
        assert isinstance(obj, dict)
        number = Number.from_dict(obj.get("number"))
        arab = from_str(obj.get("arab"))
        translation = from_str(obj.get("translation"))
        audio = Audio.from_dict(obj.get("audio"))
        image = Image.from_dict(obj.get("image"))
        tafsir = Tafsir.from_dict(obj.get("tafsir"))
        meta = Meta.from_dict(obj.get("meta"))
        return Ayah(number, arab, translation, audio, image, tafsir, meta)

    def to_dict(self) -> dict:
        result: dict = {}
        result["number"] = to_class(Number, self.number)
        result["arab"] = from_str(self.arab)
        result["translation"] = from_str(self.translation)
        result["audio"] = to_class(Audio, self.audio)
        result["image"] = to_class(Image, self.image)
        result["tafsir"] = to_class(Tafsir, self.tafsir)
        result["meta"] = to_class(Meta, self.meta)
        return result


@dataclass
class Bismillah:
    arab: str
    translation: str
    audio: Audio

    @staticmethod
    def from_dict(obj: Any) -> 'Bismillah':
        assert isinstance(obj, dict)
        arab = from_str(obj.get("arab"))
        translation = from_str(obj.get("translation"))
        audio = Audio.from_dict(obj.get("audio"))
        return Bismillah(arab, translation, audio)

    def to_dict(self) -> dict:
        result: dict = {}
        result["arab"] = from_str(self.arab)
        result["translation"] = from_str(self.translation)
        result["audio"] = to_class(Audio, self.audio)
        return result


@dataclass
class QuranModelItem:
    number: int
    number_of_ayahs: int
    name: str
    translation: str
    revelation: str
    description: str
    audio: str
    bismillah: Bismillah
    ayahs: List[Ayah]

    @staticmethod
    def from_dict(obj: Any) -> 'QuranModelItem':
        assert isinstance(obj, dict)
        number = from_int(obj.get("number"))
        number_of_ayahs = from_int(obj.get("numberOfAyahs"))
        name = from_str(obj.get("name"))
        translation = from_str(obj.get("translation"))
        revelation = from_str(obj.get("revelation"))
        description = from_str(obj.get("description"))
        audio = from_str(obj.get("audio"))
        bismillah = Bismillah.from_dict(obj.get("bismillah"))
        ayahs = from_list(Ayah.from_dict, obj.get("ayahs"))
        return QuranModelItem(number, number_of_ayahs, name, translation, revelation, description, audio, bismillah, ayahs)

    def to_dict(self) -> dict:
        result: dict = {}
        result["number"] = from_int(self.number)
        result["numberOfAyahs"] = from_int(self.number_of_ayahs)
        result["name"] = from_str(self.name)
        result["translation"] = from_str(self.translation)
        result["revelation"] = from_str(self.revelation)
        result["description"] = from_str(self.description)
        result["audio"] = from_str(self.audio)
        result["bismillah"] = to_class(Bismillah, self.bismillah)
        result["ayahs"] = from_list(lambda x: to_class(Ayah, x), self.ayahs)
        return result


def quran_model_from_dict(s: Any) -> List[QuranModelItem]:
    return from_list(QuranModelItem.from_dict, s)


def quran_model_to_dict(x: List[QuranModelItem]) -> Any:
    return from_list(lambda x: to_class(QuranModelItem, x), x)
