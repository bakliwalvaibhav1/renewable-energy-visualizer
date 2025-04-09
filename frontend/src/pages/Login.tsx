import { useState } from "react";
import { useAuth } from "../context/AuthContext";
import { useNavigate, Navigate } from "react-router-dom";
import { api } from "../library/axios";
import EcoView from "../assets/EcoView.png";

export default function Login() {
    const { isAuthenticated, login } = useAuth();
    const navigate = useNavigate();

    const [mode, setMode] = useState<"login" | "register">("login");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");

    if (isAuthenticated) {
        return <Navigate to="/dashboard" />;
    }

    const handleLogin = async (e: React.FormEvent) => {
        e.preventDefault();

        try {
            const response = await api.post(
                "/auth/login",
                new URLSearchParams({ username: email, password }),
                {
                    headers: {
                        "Content-Type": "application/x-www-form-urlencoded",
                    },
                }
            );

            login(response.data.access_token);
            navigate("/dashboard");
        } catch (err) {
            console.error("Login error:", err);
        }
    };

    const handleRegister = async (e: React.FormEvent) => {
        e.preventDefault();

        if (password !== confirmPassword) {
            alert("Passwords do not match!");
            return;
        }

        try {
            await api.post("/auth/register", { email, password });

            alert("Registration successful! You can now log in.");
            setMode("login");
        } catch (err) {
            console.error("Register error:", err);
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-green-100 via-white to-green-200">
            <div className="max-w-md w-full mx-auto p-6 shadow-xl rounded bg-white">
                <div className="flex justify-center mb-6">
                    <img
                        src={EcoView}
                        alt="EcoView Logo"
                        className="h-16 w-auto"
                    />
                </div>

                {/* Toggle Tabs */}
                <div className="flex justify-center gap-4 mb-6">
                    <button
                        type="button"
                        className={`px-4 py-2 rounded ${
                            mode === "login"
                                ? "bg-green-500 text-white"
                                : "bg-gray-200"
                        }`}
                        onClick={() => setMode("login")}
                    >
                        Login
                    </button>
                    <button
                        type="button"
                        className={`px-4 py-2 rounded ${
                            mode === "register"
                                ? "bg-green-500 text-white"
                                : "bg-gray-200"
                        }`}
                        onClick={() => setMode("register")}
                    >
                        Register
                    </button>
                </div>

                {/* Login / Register Form */}
                <form
                    onSubmit={mode === "login" ? handleLogin : handleRegister}
                    className="space-y-4"
                >
                    <input
                        type="email"
                        placeholder="Email"
                        className="w-full p-2 border rounded"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                    />

                    <input
                        type="password"
                        placeholder="Password"
                        className="w-full p-2 border rounded"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />

                    {mode === "register" && (
                        <input
                            type="password"
                            placeholder="Confirm Password"
                            className="w-full p-2 border rounded"
                            value={confirmPassword}
                            onChange={(e) =>
                                setConfirmPassword(e.target.value)
                            }
                            required
                        />
                    )}

                    <button
                        type="submit"
                        className="w-full py-2 rounded text-white bg-green-500 hover:bg-green-700"
                    >
                        {mode === "login" ? "Login" : "Register"}
                    </button>
                </form>
            </div>
        </div>
    );
}
