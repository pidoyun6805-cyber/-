# Master of Malt Watch Log

## 2026-08-05 05:52 UTC — 두 번째 실행 (실패: 사이트 자체 봇 차단, HTTP 429)

- **확인 시도한 브랜드**: Springbank (Local Barley 포함), George T. Stagg, Van Winkle/Pappy Van Winkle, Macallan, Clynelish, Daftmill (전체 6개)
- **결과**: 이전 실행(11분 전, 05:41 UTC)과 달리 이번에는 프록시 CONNECT 단계 403 차단은 사라졌습니다 (`$HTTPS_PROXY/__agentproxy/status`의 `recentRelayFailures`도 비어 있음). 하지만 masterofmalt.com 자체가 모든 요청(홈페이지, 검색 페이지, 개별 제품 페이지)에 HTTP 429와 함께 "Vercel Security Checkpoint"라는 JS 기반 봇 탐지 챌린지 페이지를 반환했습니다. WebFetch, 브라우저 User-Agent를 지정한 curl 모두 동일하게 차단됨.
- **원인**: 프록시 정책 차단이 아니라 사이트 자체의 봇 차단(Vercel Security Checkpoint)입니다. 이 챌린지를 우회하는 시도(헤더/IP 스푸핑, JS 챌린지 자동 풀이 등)는 탐지 회피(detection evasion)에 해당하여 시도하지 않았습니다.
- **WebSearch로 얻은 부가 정보**: 구글 검색 인덱스를 통해 Springbank Local Barley의 여러 빈티지/배치(예: 2025 Release 10 Year Old, 8 Year Old 2016 등) 제품명과 URL은 확인했으나, 가격이나 재고 상태(Add to basket / Notify me)는 검색 스니펫에 없어 확인 불가.
- **state.json**: 신뢰할 수 없는 재고/가격 데이터로 다음 실행에서 허위 비교가 발생하지 않도록, 제품 데이터는 비워두고 이번 실행이 실패했다는 사실(및 실패 원인이 프록시 정책 → 사이트 자체 봇 차단으로 바뀌었다는 점)만 기록했습니다.
- **알림 발송 여부**: 보내지 않음 — 직전 실행(11분 전)에서 이미 "사이트 접속 불가" 사실을 알렸고, 이번 실행도 동일한 근본 문제(접속 불가)의 연장선이라 중복 알림은 생략했습니다. 다만 실패 원인이 바뀐 점은 로그에 기록해 둡니다.
- **다음 실행을 위한 참고**: 사이트의 봇 탐지(Vercel Security Checkpoint)가 계속되는 한 자동화된 모니터링은 구조적으로 불가능합니다. 정상적인 브라우저 세션/쿠키를 통한 접근이 허용되는 방법이 마련되지 않으면 계속 실패할 것으로 예상됩니다.

## 2026-08-05 05:41 UTC — 첫 실행 (실패: 사이트 접속 차단)

- **확인 시도한 브랜드**: Springbank (Local Barley 포함), George T. Stagg, Van Winkle/Pappy Van Winkle, Macallan, Clynelish, Daftmill (전체 6개)
- **결과**: masterofmalt.com에 전혀 접속할 수 없었습니다. 6개 브랜드 조사를 위해 병렬로 실행한 조사 에이전트 전원이 모든 요청(검색 페이지, 브랜드 페이지, 홈페이지, 개별 제품 페이지)에서 HTTP 403을 보고했습니다.
- **원인 확인**: 직접 `curl`로 masterofmalt.com에 접속 시도한 결과 프록시 CONNECT 터널 단계에서 403 거부(`gateway answered 403 to CONNECT (policy denial or upstream failure)`). 프록시 상태 엔드포인트(`$HTTPS_PROXY/__agentproxy/status`)의 `recentRelayFailures` 로그에서 동일 오류가 다수 확인됨. 비교 테스트로 시도한 thewhiskyexchange.com도 동일하게 차단되어, 이 환경의 아웃바운드 프록시가 주류 판매 사이트(alcohol-retail) 카테고리 자체를 정책적으로 차단하고 있는 것으로 보입니다 (Master of Malt 사이트 자체의 봇 차단이 아님).
- **WebSearch로 얻은 부가 정보**: 구글 검색 인덱스를 통해 각 브랜드의 제품명/URL 목록은 일부 확인했으나(예: Springbank 10 Year Old Local Barley 2025 Release, George T. Stagg 2022 Release 등), 가격이나 재고 상태(Add to basket / Notify me)는 검색 스니펫에 포함되지 않아 전혀 확인하지 못했습니다.
- **state.json**: 신뢰할 수 없는 재고/가격 데이터를 저장하면 다음 실행에서 잘못된 비교(허위 신제품/재입고 알림)로 이어질 수 있어, 제품 데이터는 비워두고 이번 실행이 실패했다는 사실만 기록했습니다.
- **알림 발송 여부**: 발송함 (PushNotification) — 핵심 작업(신제품/재입고 확인)을 이번 실행에서는 전혀 수행할 수 없었기 때문에, 사이트 접속이 막혀 있다는 사실 자체를 알렸습니다.
- **다음 실행을 위한 참고**: 이 환경의 네트워크 정책이 masterofmalt.com(및 주류 판매 사이트 일반)을 계속 차단한다면 향후 실행도 동일하게 실패할 가능성이 높습니다. 프록시 정책에서 masterofmalt.com을 허용 목록에 추가하는 조치가 필요해 보입니다.
