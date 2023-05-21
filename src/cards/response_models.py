from pydantic import BaseModel, Field, HttpUrl


class ArcaneSchema(BaseModel):
    id: int = Field(..., description="serial number", example='10')
    type: str = Field(
        ...,
        description="Type of the arcane. It could be minor or major.",
        example="major"
    )
    name: str = Field(
        ...,
        description="Name of arcane in Russian",
        example='Влюбленные')
    slug: str = Field(
        ...,
        description="simple slug name of arcane",
        example="lovers"
    )
    card: HttpUrl = Field(
        ...,
        description='Outer URL of pic',
        example="https://www.taro.lv/images/uploads/167x300/18-arc-00.jpg"
    )
    brief: str = Field(
        ...,
        description="Short descriptions associated with this arcane separated by $ symbol",
        example="Безумец, Дурак, Глупец, Блаженный$Алхимик$Паломник, Пилигрим$Созидательная Сила Господа"
    )
    general: str = Field(
        ...,
        description="General descriptions",
        example="Шут всегда предупреждает о чем-то совершенно новом, что готово ворваться в жизнь, отчего в ней возникает хаос, однако как правило ничего опасного в этом нет."
    )
    personal_condition: str = Field(
        ...,
        description="Value in relation to personal condition",
        example="Импульсивные необдуманные поступки. С уверенностью можно сказать, что у Шута легко на сердце."
    )
    deep: str = Field(
        ...,
        description="Value in deep meaning",
        example="Шут – это не только «внутренний ребенок», но еще и внутренний герой! Шут олицетворяет Героя, безрассудно движущегося навстречу своей судьбе."
    )
    career: str = Field(
        ...,
        description="Career meaning",
        example="and so on for all different interpretations of the meaning of certain arcane"
    )
    finances: str = Field(
        ...,
        description="Finances meaning",
        example="and so on for all different interpretations of the meaning of certain arcane"
    )
    relations: str = Field(
        ...,
        description="Relations meaning",
        example="and so on for all different interpretations of the meaning of certain arcane"
    )
    upside_down: str = Field(
        ...,
        description="Upside down meaning",
        example="and so on for all different interpretations of the meaning of certain arcane"
    )
    combination: str = Field(
        ...,
        description="Meaning in combination with other arcanes",
        example="and so on for all different interpretations of the meaning of certain arcane"
    )
    archetypal: str = Field(
        ...,
        description="Archetypal meaning",
        example="and so on for all different interpretations of the meaning of certain arcane"
    )
    health: str = Field(
        ...,
        description="Health meaning",
        example="and so on for all different interpretations of the meaning of certain arcane"
    )
    remarks: str | None = Field(
        None,
        description="Remarks. Could be empty.",
        example="and so on for all different interpretations of the meaning of certain arcane"
    )

    class Config:
        orm_mode = True


class AllArcanesSchema(BaseModel):
    arcanes: list[ArcaneSchema] = Field(
        ...,
        description="List of arcanes"
    )
