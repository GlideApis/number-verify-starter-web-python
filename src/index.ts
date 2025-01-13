import { randomUUID } from "crypto";
import express from "express";
import { GlideClient } from "glide-sdk";
import path from "path";

interface SessionData {
    phoneNumber?: string;
    authUrl?: string;
    code?: string;
    error?: string;
}

const PORT = process.env.PORT || 4568;

const glideClient = new GlideClient();

const app = express();
app.use(express.json());
app.use(express.static(__dirname + '/static'));

let sessionData: Record<string, SessionData> = {};
let currentSessionData: SessionData | null = null;

app.get("/", (req, res) => {
    res.sendFile(path.join(__dirname, "index.html"));
});

app.get("/api/getAuthUrl", async (req, res) => {
    try {
        const phoneNumber = req.query.phoneNumber as string;
        const state = randomUUID();
        const authUrl = await glideClient.numberVerify.getAuthUrl({
            state,
            useDevNumber: phoneNumber
        });
        sessionData[state] = {phoneNumber, authUrl};
        const response = {
            authUrl
        };
        res.json(response);
    } catch (error) {
        console.error(error);
        res.status(500).json({error: (error as Error).message});
    }
});

app.get("/api/getSessionData", async (req, res) => {
    try {
        if (!currentSessionData) {
            res.json({});
            return;
        }
        res.json(currentSessionData);
    } catch (error) {
        console.error(error);
        res.status(500).json({error: (error as Error).message});
    } finally {
        sessionData = {};
        currentSessionData = null;
    }
});

app.get("/callback", async (req, res) => {
    try {
        const code = req.query.code as string;
        const state = req.query.state as string;
        const error = req.query.error as string;
        if (!sessionData[state]) {
            sessionData[state] = {
                error: 'No session data found for state'
            };
            console.log('No session data found for state', state);
            // redirect to home page
            res.redirect('/');
            return;
        }
        sessionData[state].code = code;
        if (error) {
            const errorDescription = req.query.error_description as string;
            sessionData[state].error = errorDescription;
        }
        currentSessionData = sessionData[state];
        res.sendFile(path.join(__dirname, "static/index.html"));
    } catch (error) {
        console.error(error);
        res.status(500).json({error: (error as Error).message});
    }
});

app.post("/api/verifyNumber", async (req, res) => {
    try {
       const {code, phoneNumber} = req.body;
        const userClient = await glideClient.numberVerify.forUser({
            code,
            phoneNumber
        });
        const operator = await userClient.getOperator();
        const verifyRes = await userClient.verifyNumber();
        res.json({
            operator,
            verifyRes
        });
    } catch (error) {
        console.error(error);
        res.status(500).json({error: (error as Error).message});
    }
});

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
  