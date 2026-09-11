# abandon-cart
abandon cart demonstration

flowchart LR
    %% Frontend Experience
    subgraph Frontend [User Browser / Web Experience]
    A[index.html<br/>Failed Checkout Flow]
    B[resolution.html<br/>Successful Checkout Flow]
end

%% Observability & Digital Experience Intelligence
    subgraph Capture [Digital Experience Intelligence]
    FS[FullStory<br/>Session Replay & Custom Events]
end

%% Backend Automation & Messaging
    subgraph Infrastructure [GCP & Notification Services]
        CR[GCP Cloud Run<br/>Webhook Receiver Node.js/Python]
        TW[Twilio API<br/>SMS Dispatch]
end

%% Interactions
    A -- Captures Dead Click / Error Event --> FS
    B -- Captures Purchase Success Event --> FS
    FS -- Alert / Event Webhook Payload --> CR
    CR -- Triggers Text Message --> TW
    TW -- SMS Alert Sent --> Support[Support / Engineering Team]

%% Styling
    style A fill:#ffdddd,stroke:#f00,stroke-width:2px
    style B fill:#ddffdd,stroke:#0f0,stroke-width:2px
    style FS fill:#f0f,stroke:#333,stroke-width:1px,color:#fff
    style CR fill:#4285F4,stroke:#333,stroke-width:1px,color:#fff
    style TW fill:#F22F46,stroke:#333,stroke-width:1px,color:#fff
