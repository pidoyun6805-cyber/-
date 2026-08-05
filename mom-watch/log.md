# Master of Malt Watch Log

## 2026-08-05 06:20 UTC — 2회차 실행 (실패: 사이트가 브라우저 자동화 자체를 차단)

- **확인 시도한 브랜드**: Springbank (Local Barley 포함), George T. Stagg, Van Winkle/Pappy Van Winkle, Macallan, Clynelish, Daftmill (전체 6개)
- **접속 방식**: 지시된 대로 Playwright 헤드리스 브라우저(Chromium, `/opt/pw-browsers/chromium`) 사용. 데스크톱 Chrome User-Agent로 홈페이지(`/`), 검색 페이지(`/search/?query=Springbank`), 브랜드 페이지(`/whiskies/scotch-whisky/springbank-whisky/`)에 순차 접속 시도, 총 4회 반복 시도(`--disable-http2` 옵션 포함/미포함 모두 시도).
- **결과**: 시도한 모든 URL에서 예외 없이 `net::ERR_CONNECTION_RESET` 발생. 사이트에 전혀 접속하지 못함.
- **이전 실행과의 차이점 (중요)**: 지난 실행(첫 실행, 05:41 UTC)은 아웃바운드 프록시 정책 자체가 masterofmalt.com CONNECT 터널을 403으로 거부해서 실패했던 것과 달리, 이번에는 프록시 상태(`recentRelayFailures`)에 masterofmalt.com 관련 거부 기록이 전혀 없었고, 오히려 같은 URL들에 대해 단순 `curl` 요청(같은 User-Agent, HTTP/2 포함)은 전부 정상적으로 네트워크에 도달해 HTTP 429(요청 제한) 응답을 받았습니다. 즉, **네트워크/프록시 단은 더 이상 막혀있지 않지만, 사이트 자체의 봇 탐지 시스템이 Playwright/Chromium 같은 실제 브라우저 엔진의 연결만 골라서 강제 종료(reset)시키는 것으로 보입니다.** (JA3/TLS 핸드셰이크 또는 HTTP/2 프레임 패턴으로 자동화 브라우저를 식별해 차단하는 전형적인 WAF/봇 차단 동작으로 추정)
- **시도하지 않은 것**: 스텔스 플러그인, TLS 핑거프린트 위장 등 탐지 회피 기법은 시도하지 않았습니다. 작업 지침대로 차단 상황을 있는 그대로 기록하고 알리는 것으로 마무리했습니다.
- **WebSearch로 얻은 참고 정보 (미검증, 신제품/재입고 판단에 사용하지 않음)**: 구글 인덱스에서 각 브랜드의 최근 제품 페이지 URL은 확인했지만(예: Macallan 2000 bottled 2026 Speymalt, Clynelish 12yo 2013 Lady of the Glen, Daftmill 2012 Winter Batch, Springbank Local Barley 2026 관련 서드파티 리테일러 언급 등), 이 정보들은 실시간 재고/가격 상태를 반영하지 않으므로 신제품·재입고 알림 판단에는 전혀 사용하지 않았습니다.
- **state.json**: 이전과 마찬가지로 신뢰할 수 없는 재고/가격 데이터를 저장하지 않고, 이번 실행의 구체적인 실패 원인만 갱신해 기록했습니다.
- **알림 발송 여부**: 발송함 (PushNotification) — 실패 원인이 지난 실행과 다른 새로운 진단 정보(프록시 차단 → 사이트 자체의 브라우저 자동화 차단으로 전환)이므로 중복 알림 생략 조건에 해당하지 않는다고 판단했습니다.
- **다음 실행을 위한 참고**: 만약 다음 실행에서도 동일하게 Playwright 연결이 재설정된다면, masterofmalt.com이 헤드리스 브라우저 자동화를 지속적으로 차단하고 있다는 뜻입니다. 이 경우 정기적인 자동 모니터링이 구조적으로 어려울 수 있으므로, 사용자가 접속 방식(예: 실제 사용자 세션/쿠키 재사용, 다른 네트워크 경로 등)에 대한 판단을 내려야 할 수 있습니다.

## 2026-08-05 05:41 UTC — 첫 실행 (실패: 사이트 접속 차단)

- **확인 시도한 브랜드**: Springbank (Local Barley 포함), George T. Stagg, Van Winkle/Pappy Van Winkle, Macallan, Clynelish, Daftmill (전체 6개)
- **결과**: masterofmalt.com에 전혀 접속할 수 없었습니다. 6개 브랜드 조사를 위해 병렬로 실행한 조사 에이전트 전원이 모든 요청(검색 페이지, 브랜드 페이지, 홈페이지, 개별 제품 페이지)에서 HTTP 403을 보고했습니다.
- **원인 확인**: 직접 `curl`로 masterofmalt.com에 접속 시도한 결과 프록시 CONNECT 터널 단계에서 403 거부(`gateway answered 403 to CONNECT (policy denial or upstream failure)`). 프록시 상태 엔드포인트(`$HTTPS_PROXY/__agentproxy/status`)의 `recentRelayFailures` 로그에서 동일 오류가 다수 확인됨. 비교 테스트로 시도한 thewhiskyexchange.com도 동일하게 차단되어, 이 환경의 아웃바운드 프록시가 주류 판매 사이트(alcohol-retail) 카테고리 자체를 정책적으로 차단하고 있는 것으로 보입니다 (Master of Malt 사이트 자체의 봇 차단이 아님).
- **WebSearch로 얻은 부가 정보**: 구글 검색 인덱스를 통해 각 브랜드의 제품명/URL 목록은 일부 확인했으나(예: Springbank 10 Year Old Local Barley 2025 Release, George T. Stagg 2022 Release 등), 가격이나 재고 상태(Add to basket / Notify me)는 검색 스니펫에 포함되지 않아 전혀 확인하지 못했습니다.
- **state.json**: 신뢰할 수 없는 재고/가격 데이터를 저장하면 다음 실행에서 잘못된 비교(허위 신제품/재입고 알림)로 이어질 수 있어, 제품 데이터는 비워두고 이번 실행이 실패했다는 사실만 기록했습니다.
- **알림 발송 여부**: 발송함 (PushNotification) — 핵심 작업(신제품/재입고 확인)을 이번 실행에서는 전혀 수행할 수 없었기 때문에, 사이트 접속이 막혀 있다는 사실 자체를 알렸습니다.
- **다음 실행을 위한 참고**: 이 환경의 네트워크 정책이 masterofmalt.com(및 주류 판매 사이트 일반)을 계속 차단한다면 향후 실행도 동일하게 실패할 가능성이 높습니다. 프록시 정책에서 masterofmalt.com을 허용 목록에 추가하는 조치가 필요해 보입니다.
