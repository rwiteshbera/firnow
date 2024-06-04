from asyncio import StreamReader
from typing import Callable, Optional

if __name__ == "__main__":
    import asyncio

    async def read_stream(st: Optional[StreamReader], cb: Callable[[str], None]):
        if st is None:
            return

        while True:
            line = await st.readline()
            if not line:
                break
            cb(line.decode().strip())

    async def main():
        auth_service = await asyncio.create_subprocess_shell(
            "python -m services.auth",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        general_service = await asyncio.create_subprocess_shell(
            "python -m services.general",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        id_service = await asyncio.create_subprocess_shell(
            "py -m services.id",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        location_service = await asyncio.create_subprocess_shell(
            "python -m services.location",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        docs_service = await asyncio.create_subprocess_shell(
            "redocly preview-docs --port=8080",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        log_tasks = [
            asyncio.create_task(read_stream(auth_service.stdout, lambda x: print(x))),
            asyncio.create_task(read_stream(auth_service.stderr, lambda x: print(x))),
            asyncio.create_task(
                read_stream(general_service.stdout, lambda x: print(x))
            ),
            asyncio.create_task(
                read_stream(general_service.stderr, lambda x: print(x))
            ),
            asyncio.create_task(read_stream(id_service.stdout, lambda x: print(x))),
            asyncio.create_task(read_stream(id_service.stderr, lambda x: print(x))),
            asyncio.create_task(
                read_stream(location_service.stdout, lambda x: print(x))
            ),
            asyncio.create_task(
                read_stream(location_service.stderr, lambda x: print(x))
            ),
            asyncio.create_task(read_stream(docs_service.stdout, lambda x: print(x))),
            asyncio.create_task(read_stream(docs_service.stderr, lambda x: print(x))),
        ]

        service_tasks = [
            asyncio.create_task(auth_service.wait()),
            asyncio.create_task(general_service.wait()),
            asyncio.create_task(id_service.wait()),
            asyncio.create_task(location_service.wait()),
            asyncio.create_task(docs_service.wait()),
        ]

        try:
            await asyncio.gather(*log_tasks)
            await asyncio.gather(*service_tasks)

        except asyncio.CancelledError:
            for log_task in log_tasks:
                log_task.cancel()

            for service_task in service_tasks:
                service_task.cancel()

        finally:
            auth_service._transport.close()  # type: ignore
            auth_service.kill()
            general_service._transport.close()  # type: ignore
            general_service.kill()
            id_service._transport.close()  # type: ignore
            id_service.kill()
            location_service._transport.close()  # type: ignore
            location_service.kill()
            docs_service._transport.close()  # type: ignore
            docs_service.kill()

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        ...
