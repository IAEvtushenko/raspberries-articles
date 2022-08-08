from fastapi import FastAPI
from starlette import status

from raspberries.adapters.dto import GenericCreateDto, GenericUpdateDto, GenericRetrieveDeleteDto
from raspberries.services.base import get_service

app = FastAPI()


@app.post("/{service_id}/create", status_code=status.HTTP_201_CREATED)
async def create(service_id: str, data: GenericCreateDto):
    service = get_service(service_id)
    return await service.create(data)


@app.post("/{service_id}/update")
async def update(service_id: str, data: GenericUpdateDto):
    service = get_service(service_id)
    return await service.update(data)


@app.get("/{service_id}/get")
async def retrieve(service_id: str, data: GenericRetrieveDeleteDto):
    service = get_service(service_id)
    return await service.retrieve(data.ids)


@app.get("/{service_id}/delete")
async def delete(service_id: str, data: GenericRetrieveDeleteDto):
    service = get_service(service_id)
    await service.delete(data.ids)
    return {"status": "ok"}
