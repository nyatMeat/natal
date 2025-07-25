"""
This module provides statistical analysis and report generation for natal charts.
"""

from enum import Enum
from natal.classes import Aspect, House, MovableBody, Planet
from natal.config import Config, get_translation
from natal.const import (
    ASPECT_MEMBERS,
    ELEMENT_MEMBERS,
    HOUSE_MEMBERS,
    MODALITY_MEMBERS,
    POLARITY_MEMBERS,
    SIGN_MEMBERS,
    VERTEX_MEMBERS,
)
from natal.data import Data
from pydantic import BaseModel, Field


class DistKind(str, Enum):
    """Distribution kind for statistical analysis."""

    element = "element"
    modality = "modality"
    polarity = "polarity"


class ReportKind(str, Enum):
    """Report kind for selecting which report to generate."""

    full = "full"
    composite = "composite"


Grid = list[list[str | int | float]]


class StatData(BaseModel):
    """Data structure for statistical information."""

    title: str
    grid: Grid = Field(default_factory=list)


class Stats:
    """
    This class handles statistical calculations and report generation for natal chart data.
    """

    data1: Data
    data2: Data | None = None

    def __init__(self, data1: Data, data2: Data | None = None, lang: str = "en"):
        """Initialize a Stats object.

        Args:
            data1: Primary chart data
            data2: Secondary chart data for composite charts
            lang: Language for the reports (ru, en, ko, es)
        """
        self.data1 = data1
        self.data2 = data2
        self.lang = lang

        self.composite_pairs = []
        if self.data2 is not None:
            self.composite_pairs = self.data1.composite_aspects_pairs(self.data2)

        self.composite_aspects = self.data1.calculate_aspects(self.composite_pairs)

    def _t(self, text: str) -> str:
        """Helper method for translation."""
        return get_translation(text, self.lang)

    def dignity_of(self, body: MovableBody, data: Data) -> str:
        """Get the dignity of a celestial body."""
        sign = body.sign
        dignity_type = ""

        if sign.ruler == body.name or sign.classic_ruler == body.name:
            dignity_type = "ruler"
        elif sign.detriment == body.name or sign.classic_detriment == body.name:
            dignity_type = "detriment"
        elif sign.exaltation == body.name:
            dignity_type = "exaltation"
        elif sign.fall == body.name:
            dignity_type = "fall"

        return self._t(dignity_type) if dignity_type else ""

    def basic_info(self, data: Data) -> StatData:
        """Generate basic information about celestial bodies."""
        grid = []
        for body in data.planets:
            grid.append(
                [
                    self._t(body.name),
                    self._t(body.sign.name),
                    body.dms,
                    f"h{body.house_of(data)}",
                    self.dignity_of(body, data),
                ]
            )
        return StatData(title=self._t("basic_info"), grid=grid)

    def distribution(self, dist_kind: DistKind) -> StatData:
        """Generate distribution statistics for elements, modalities, or polarities."""
        title = f"{self._t(dist_kind.value)} {self._t('distribution')}"
        grid = []
        items = globals()[f"{dist_kind.value.upper()}_MEMBERS"]
        for item in items:
            count = 0
            for planet in self.data1.planets:
                if getattr(planet.sign, dist_kind.value) == item.name:
                    count += 1
            percentage = (count / len(self.data1.planets)) * 100
            grid.append(
                [
                    self._t(item.name),
                    f"{count}",
                    f"{percentage:.2f}%",
                ]
            )
        return StatData(title=title, grid=grid)

    def celestial_body(self, body: Planet) -> StatData:
        """Generate detailed information about a celestial body."""
        title = f"{self._t('aspects')} for {self._t(body.name)}"
        grid = [
            [self._t(body.sign.name), body.dms],
            [f"h{body.house_of(self.data1)}", self.dignity_of(body, self.data1)],
        ]
        return StatData(title=title, grid=grid)

    def data2_celestial_body(self, body: Planet) -> StatData:
        """Generate detailed information about a celestial body for the secondary data source."""
        title = f"{self._t('aspects')} for {self._t(body.name)}"
        grid = [
            [self._t(body.sign.name), body.dms],
            [
                f"h{body.house_of(self.data2)} in synastry",
                self.dignity_of(body, self.data2),
            ],
        ]
        return StatData(title=title, grid=grid)

    def house(self, house: House) -> StatData:
        """Generate information about a house."""
        title = self._t(f"house {house.value}")
        grid = [[self._t(house.sign.name), f"{self._t('ruler')}: {self._t(house.ruler)}"]]
        return StatData(title=title, grid=grid)

    def quadrant(self, quadrant_num: int) -> StatData:
        """Generate information about a quadrant."""
        title = self._t(f"quadrant {quadrant_num}")
        grid = []
        for body in self.data1.quadrants[quadrant_num - 1]:
            grid.append([self._t(body.name), self._t(body.sign.name), body.dms])
        return StatData(title=title, grid=grid)

    def hemisphere(self, hemisphere: str) -> StatData:
        """Generate information about a hemisphere."""
        title = f"{self._t(hemisphere)} {self._t('hemisphere')}"
        grid = []
        for body in getattr(self.data1, hemisphere):
            grid.append([self._t(body.name), self._t(body.sign.name), body.dms])
        return StatData(title=title, grid=grid)

    def aspect(self, aspect: Aspect) -> StatData:
        """Generate information about an aspect."""
        title = self._t(aspect.aspect_member.name)
        grid = [
            [
                self._t(aspect.body1.name),
                self._t(aspect.body2.name),
                f"{aspect.orb:.2f}°",
            ]
        ]
        return StatData(title=title, grid=grid)

    def composite_aspect(self, aspect: Aspect) -> StatData:
        """Generate information about a composite aspect."""
        title = self._t(aspect.aspect_member.name)
        grid = [
            [
                self._t(aspect.body1.name),
                self._t(aspect.body2.name),
                f"{aspect.orb:.2f}°",
            ]
        ]
        return StatData(title=title, grid=grid)

    def cross_ref(self, body1: MovableBody, body2: MovableBody) -> StatData:
        """Generate cross-reference information between two celestial bodies."""
        title = f"{self._t(body1.name)}-{self._t(body2.name)}"
        grid = [
            [self._t(body1.sign.name), body1.dms],
            [self._t(body2.sign.name), body2.dms],
        ]
        return StatData(title=title, grid=grid)

    def full_report(self) -> list[StatData]:
        """Generate a full report."""
        report = [self.basic_info(self.data1)]
        for kind in DistKind:
            report.append(self.distribution(kind))
        report.append(StatData(title=self._t("celestial_bodies")))
        for body in self.data1.planets:
            report.append(self.celestial_body(body))
        report.append(StatData(title=self._t("houses")))
        for house in self.data1.houses:
            report.append(self.house(house))
        report.append(StatData(title=self._t("quadrants")))
        for i in range(1, 5):
            report.append(self.quadrant(i))
        report.append(StatData(title=self._t("hemispheres")))
        for hemisphere in ["east", "west", "north", "south"]:
            report.append(self.hemisphere(hemisphere))
        report.append(StatData(title=self._t("aspects")))
        for aspect in self.data1.aspects:
            report.append(self.aspect(aspect))
        return report

    def table_of(self, report_kind: ReportKind) -> list[StatData]:
        """Generate a table of contents for a report."""
        if report_kind == ReportKind.full:
            return self.full_report()
        if report_kind == ReportKind.composite:
            return self.composite_report()
        return []
