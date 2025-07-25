from enum import StrEnum
from pydantic import BaseModel
from types import SimpleNamespace
from typing import Any, Iterator, Literal, Mapping

ThemeType = Literal["light", "dark", "mono"]


class Dictable(Mapping):
    """
    Protocols for subclasses to behave like a dict.
    """

    def __getitem__(self, key: str):
        return getattr(self, key)

    def __setitem__(self, key: str, value: Any) -> None:
        setattr(self, key, value)

    def __iter__(self) -> Iterator[str]:
        return iter(self.__dict__)

    def __len__(self) -> int:
        return len(self.__dict__)

    def update(self, other: Mapping[str, Any] | None = None, **kwargs) -> None:
        """
        Update the attributes with elements from another mapping or from key/value pairs.

        Args:
            other (Mapping[str, Any] | None): A mapping object to update from.
            **kwargs: Additional key/value pairs to update with.
        """
        if other is not None:
            for key, value in other.items():
                setattr(self, key, value)
        for key, value in kwargs.items():
            setattr(self, key, value)


class DotDict(SimpleNamespace, Dictable):
    """
    Extends SimpleNamespace to allow for unpacking and subscript notation access.
    """

    pass


class ModelDict(BaseModel, Dictable):
    """
    Extends BaseModel to allow for unpacking and subscript notation access.
    """

    # override to return keys, otherwise BaseModel.__iter__ returns key value pairs
    def __iter__(self) -> Iterator[str]:
        return iter(self.__dict__)


class HouseSys(StrEnum):
    Placidus = "P"
    Koch = "K"
    Equal = "E"
    Campanus = "C"
    Regiomontanus = "R"
    Porphyry = "P"
    Whole_Sign = "W"


class Orb(ModelDict):
    """default orb for natal chart"""

    conjunction: int = 7
    opposition: int = 6
    trine: int = 6
    square: int = 6
    sextile: int = 5
    quincunx: int = 0


class Theme(ModelDict):
    """
    Default colors for the chart.
    """

    fire: str = "#ef476f"  # fire, square, Asc
    earth: str = "#ffd166"  # earth, MC
    air: str = "#06d6a0"  # air, trine
    water: str = "#81bce7"  # water, opposition
    points: str = "#118ab2"  # lunar nodes, sextile
    asteroids: str = "#AA96DA"  # asteroids, quincunx
    positive: str = "#FFC0CB"  # positive
    negative: str = "#AD8B73"  # negative
    others: str = "#FFA500"  # conjunction
    transparency: float = 0.1
    foreground: str
    background: str
    dim: str


class LightTheme(Theme):
    """
    Default light colors.
    """

    foreground: str = "#758492"
    background: str = "#FFFDF1"
    dim: str = "#A4BACD"


class DarkTheme(Theme):
    """
    Default dark colors.
    """

    foreground: str = "#F7F3F0"
    background: str = "#343a40"
    dim: str = "#515860"


class Display(ModelDict):
    """
    Display settings for celestial bodies.
    """

    sun: bool = True
    moon: bool = True
    mercury: bool = True
    venus: bool = True
    mars: bool = True
    jupiter: bool = True
    saturn: bool = True
    uranus: bool = True
    neptune: bool = True
    pluto: bool = True
    asc_node: bool = True
    chiron: bool = False
    ceres: bool = False
    pallas: bool = False
    juno: bool = False
    vesta: bool = False
    asc: bool = True
    ic: bool = False
    dsc: bool = False
    mc: bool = True


class Chart(ModelDict):
    """
    Chart configuration settings.
    """

    stroke_width: int = 1
    stroke_opacity: float = 1
    font: str = "sans-serif"
    font_size_fraction: float = 0.55
    inner_min_degree: float = 9
    outer_min_degree: float = 8
    margin_factor: float = 0.04
    ring_thickness_fraction: float = 0.15
    # hard-coded 2.2 and 600 due to the original symbol svg size = 20x20
    scale_adj_factor: float = 600
    pos_adj_factor: float = 2.2

TRANSLATIONS = {
    # Planets
    "sun": {"ru": "Солнце", "ko": "태양", "es": "Sol"},
    "moon": {"ru": "Луна", "ko": "달", "es": "Luna"},
    "mercury": {"ru": "Меркурий", "ko": "수성", "es": "Mercurio"},
    "venus": {"ru": "Венера", "ko": "금성", "es": "Venus"},
    "mars": {"ru": "Марс", "ko": "화성", "es": "Marte"},
    "jupiter": {"ru": "Юпитер", "ko": "목성", "es": "Júpiter"},
    "saturn": {"ru": "Сатурн", "ko": "토성", "es": "Saturno"},
    "uranus": {"ru": "Уран", "ko": "천왕성", "es": "Urano"},
    "neptune": {"ru": "Нептун", "ko": "해왕성", "es": "Neptuno"},
    "pluto": {"ru": "Плутон", "ko": "명왕성", "es": "Plutón"},
    # Extras
    "asc_node": {"ru": "Восходящий узел", "ko": "상승 노드", "es": "Nodo ascendente"},
    "chiron": {"ru": "Хирон", "ko": "키론", "es": "Quirón"},
    "ceres": {"ru": "Церера", "ko": "세레스", "es": "Ceres"},
    "pallas": {"ru": "Паллада", "ko": "팔라스", "es": "Pallas"},
    "juno": {"ru": "Юнона", "ko": "주노", "es": "Juno"},
    "vesta": {"ru": "Веста", "ko": "베스타", "es": "Vesta"},
    # Signs
    "aries": {"ru": "Овен", "ko": "양자리", "es": "Aries"},
    "taurus": {"ru": "Телец", "ko": "황소자리", "es": "Tauro"},
    "gemini": {"ru": "Близнецы", "ko": "쌍둥이자리", "es": "Géminis"},
    "cancer": {"ru": "Рак", "ko": "게자리", "es": "Cáncer"},
    "leo": {"ru": "Лев", "ko": "사자자리", "es": "Leo"},
    "virgo": {"ru": "Дева", "ko": "처녀자리", "es": "Virgo"},
    "libra": {"ru": "Весы", "ko": "천칭자리", "es": "Libra"},
    "scorpio": {"ru": "Скорпион", "ko": "전갈자리", "es": "Escorpio"},
    "sagittarius": {"ru": "Стрелец", "ko": "사수자리", "es": "Sagitario"},
    "capricorn": {"ru": "Козерог", "ko": "염소자리", "es": "Capricornio"},
    "aquarius": {"ru": "Водолей", "ko": "물병자리", "es": "Acuario"},
    "pisces": {"ru": "Рыбы", "ko": "물고기자리", "es": "Piscis"},
    # Aspects
    "conjunction": {"ru": "Соединение", "ko": "합", "es": "Conjunción"},
    "opposition": {"ru": "Оппозиция", "ko": "충", "es": "Oposición"},
    "trine": {"ru": "Трин", "ko": "삼각", "es": "Trígono"},
    "square": {"ru": "Квадрат", "ko": "사각", "es": "Cuadratura"},
    "sextile": {"ru": "Секстиль", "ko": "육각", "es": "Sextil"},
    "quincunx": {"ru": "Квинконкс", "ko": "퀸컹크스", "es": "Quincuncio"},
    # Elements
    "fire": {"ru": "Огонь", "ko": "불", "es": "Fuego"},
    "earth": {"ru": "Земля", "ko": "흙", "es": "Tierra"},
    "air": {"ru": "Воздух", "ko": "공기", "es": "Aire"},
    "water": {"ru": "Вода", "ko": "물", "es": "Agua"},
    # Modalities
    "cardinal": {"ru": "Кардинальный", "ko": "활동궁", "es": "Cardinal"},
    "fixed": {"ru": "Фиксированный", "ko": "고정궁", "es": "Fijo"},
    "mutable": {"ru": "Мутабельный", "ko": "변통궁", "es": "Mutable"},
    # Polarities
    "positive": {"ru": "Позитивная", "ko": "양성", "es": "Positivo"},
    "negative": {"ru": "Негативная", "ko": "음성", "es": "Negativo"},
    # Vertices
    "asc": {"ru": "Асцендент", "ko": "상승점", "es": "Ascendente"},
    "dsc": {"ru": "Десцендент", "ko": "하강점", "es": "Descendente"},
    "mc": {"ru": "Середина неба", "ko": "중천", "es": "Medio Cielo"},
    "ic": {"ru": "Надир", "ko": "천저", "es": "Imum Coeli"},
    # Dignities
    "ruler": {"ru": "Управитель", "ko": "지배성", "es": "Regente"},
    "detriment": {"ru": "Изгнание", "ko": "손상", "es": "Detrimento"},
    "exaltation": {"ru": "Экзальтация", "ko": "고양", "es": "Exaltación"},
    "fall": {"ru": "Падение", "ko": "쇠약", "es": "Caída"},
    # Other
    "house": {"ru": "Дом", "ko": "하우스", "es": "Casa"},
    "distribution": {"ru": "Распределение", "ko": "분포", "es": "Distribución"},
    "quadrant": {"ru": "Квадрант", "ko": "사분면", "es": "Cuadrante"},
    "hemisphere": {"ru": "Полушарие", "ko": "반구", "es": "Hemisferio"},
    "basic_info": {"ru": "Основная информация", "ko": "기본 정보", "es": "Información básica"},
    "element_distribution": {"ru": "Распределение по стихиям", "ko": "원소 분포", "es": "Distribución de elementos"},
    "modality_distribution": {"ru": "Распределение по модальностям", "ko": "양상 분포", "es": "Distribución de modalidades"},
    "polarity_distribution": {"ru": "Распределение по полярностям", "ko": "극성 분포", "es": "Distribución de polaridades"},
    "celestial_bodies": {"ru": "Небесные тела", "ko": "천체", "es": "Cuerpos celestes"},
    "houses": {"ru": "Дома", "ko": "하우스", "es": "Casas"},
    "quadrants": {"ru": "Квадранты", "ko": "사분면", "es": "Cuadrantes"},
    "hemispheres": {"ru": "Полушария", "ko": "반구", "es": "Hemisferios"},
    "aspects": {"ru": "Аспекты", "ko": "각", "es": "Aspectos"},
    "composite_aspects": {"ru": "Композитные аспекты", "ko": "합성 각", "es": "Aspectos compuestos"},
    "cross_aspects": {"ru": "Перекрестные аспекты", "ko": "교차 각", "es": "Aspectos cruzados"},
}

def get_translation(text: str, lang: str) -> str:
    """
    Get the translation for a given text and language.
    Falls back to English if the translation is not available.
    """
    if lang == "en":
        return text.replace("_", " ").title()

    key = text.lower()

    # For cases like "house 1", "quadrant 1"
    parts = key.split()
    if len(parts) > 1 and parts[1].isdigit():
        base_key = parts[0]
        if base_key in TRANSLATIONS:
            base_translation = TRANSLATIONS[base_key].get(lang, base_key.title())
            return f"{base_translation} {parts[1]}"

    return TRANSLATIONS.get(key, {}).get(lang, text.replace("_", " ").title())


class Config(ModelDict):
    """
    Package configuration model.
    """

    theme_type: ThemeType = "dark"
    house_sys: HouseSys = HouseSys.Placidus
    orb: Orb = Orb()
    light_theme: LightTheme = LightTheme()
    dark_theme: DarkTheme = DarkTheme()
    display: Display = Display()
    chart: Chart = Chart()

    @property
    def theme(self) -> Theme:
        """
        Return theme colors based on the theme type.

        Returns:
            Theme: The theme colors.
        """
        match self.theme_type:
            case "light":
                return self.light_theme
            case "dark":
                return self.dark_theme
            case "mono":
                kwargs = {key: "#888888" for key in self.light_theme.model_dump()}
                kwargs["background"] = "#FFFFFF"
                kwargs["transparency"] = 0
                return Theme(**kwargs)


